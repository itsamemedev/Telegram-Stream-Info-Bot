# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
  9856  GET              /                                                dashboard
 11903  GET              /api/abo/status                                  api_abo_status
 11857  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 10644  GET              /api/automation/status                           api_automation_status
 10666  POST             /api/automation/toggle                           api_automation_toggle
 19153  GET              /api/channel/categories                          api_channel_categories
 19159  POST             /api/channel/set                                 api_channel_set
 19006  GET              /api/channels/status                             api_channels_status
 18680  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 18663  GET              /api/clips                                       api_clips
 18709  POST/DELETE      /api/clips/clear                                 api_clips_clear
 18588  GET              /api/debug/threads                               api_debug_threads
 11868  GET              /api/events                                      api_events
 11352  GET              /api/events/stream                               api_events_stream
 11179  GET              /api/health                                      api_health
 18622  POST             /api/highlights/config                           api_highlights_config
  9790  POST             /api/login                                       dashboard_login_submit
 12193  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11267  GET              /api/notify/status                               api_notify_status
 11278  POST             /api/notify/test                                 api_notify_test
 11957  GET              /api/proxy/heatmap                               api_proxy_heatmap
 11934  GET              /api/proxy/trend                                 api_proxy_trend
 18729  GET              /api/tts/<fn>                                    api_tts_file
 19504  GET              /api/upload_window                               api_upload_window
 11469  GET              /archive/<int:eid>/download                      archive_download
 11497  GET              /download/<int:recording_id>                     download
 11426  GET              /health                                          health
 18534  GET              /healthz                                         healthz
  9781  GET              /login                                           dashboard_login_page
  9811  GET              /logout                                          dashboard_logout
  9818  GET              /manifest.webmanifest                            pwa_manifest
 19477  GET              /overlay                                         overlay_page
  9842  GET              /pwa-icon-<variant>.png                          pwa_icon
  9828  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (335)

```
   182  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   410  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
  1003  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   743  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   874  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   854  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   892  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   816  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   356  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   367  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   377  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   400  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   407  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   418  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   551  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   649  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1241  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1273  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   340  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   956  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   936  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1109  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1157  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1208  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1067  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   911  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   499  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   763  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   645  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   628  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   620  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   456  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   472  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   807  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   374  GET              /api/archive/scan                                api_archive_scan   [nc/routes/archive.py]
   405  POST             /api/archive/scan/adopt                          api_archive_scan_adopt   [nc/routes/archive.py]
   772  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   792  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   679  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    49  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    78  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   216  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   241  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   246  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
   163  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    99  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   222  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   120  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   342  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   328  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   350  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   174  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   406  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   397  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   314  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   190  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   231  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   243  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   372  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   281  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   267  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   379  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
   286  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   208  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   174  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   157  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   387  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   364  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
   198  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   131  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   116  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    93  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   158  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    80  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    81  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    53  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
   161  GET              /api/checks                                      api_checks   [nc/routes/auskunft.py]
    40  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    52  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    52  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    87  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   122  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   431  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   434  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   419  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   239  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   195  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    73  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    80  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   485  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   260  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   287  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   380  POST             /api/db/restore/apply                            api_db_restore_apply   [nc/routes/settings.py]
   324  GET              /api/db/restore/list                             api_db_restore_list   [nc/routes/settings.py]
   342  POST             /api/db/restore/prepare                          api_db_restore_prepare   [nc/routes/settings.py]
   247  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
   164  GET              /api/defense/attacks                             api_defense_attacks   [nc/routes/abwehr.py]
   125  GET              /api/defense/crowdsec                            api_defense_crowdsec   [nc/routes/abwehr.py]
   146  GET              /api/defense/fail2ban                            api_defense_fail2ban   [nc/routes/abwehr.py]
    91  GET              /api/defense/overview                            api_defense_overview   [nc/routes/abwehr.py]
   244  POST             /api/discord/announce                            api_discord_announce   [nc/routes/discord.py]
   170  GET              /api/discord/clips_week                          api_discord_clips_week   [nc/routes/discord.py]
   188  GET              /api/discord/community                           api_discord_community   [nc/routes/discord.py]
   160  GET              /api/discord/invite                              api_discord_invite   [nc/routes/discord.py]
    63  GET              /api/discord/overview                            api_discord_overview   [nc/routes/discord.py]
   136  POST             /api/discord/webhook_test                        api_discord_webhook_test   [nc/routes/discord.py]
    79  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
   112  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   120  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    60  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   136  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
   194  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   179  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    90  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   112  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   133  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
   150  POST             /api/evolution/proposals/bulk                    api_evolution_bulk   [nc/routes/evolution.py]
    80  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   209  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    44  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   200  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   220  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   247  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
   382  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   284  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   402  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   397  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   473  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
    64  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    53  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   307  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    77  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   168  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    43  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   150  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   125  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   189  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    76  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    99  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   223  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   222  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   244  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
   103  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   171  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   149  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    85  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   128  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   178  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   119  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   167  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   184  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   215  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   191  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   251  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   221  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    82  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   235  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
   416  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
    78  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
   103  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   113  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    52  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    70  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   225  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
   100  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    66  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    77  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   142  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   137  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   128  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    53  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    92  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   257  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   324  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   352  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   203  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   270  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   505  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    80  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   168  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   151  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   391  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   225  GET              /api/outcomes                                    api_outcomes   [nc/routes/auskunft.py]
   210  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   193  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
    94  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   177  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   460  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   435  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   296  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   142  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   944  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
  1053  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
  1081  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
  1101  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   931  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   993  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   980  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   961  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   335  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   606  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   601  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   649  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   532  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   859  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   623  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   586  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   559  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   833  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   703  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   792  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   698  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   631  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   411  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   876  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   499  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   754  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   909  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   894  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   455  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   693  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   679  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   662  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   719  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
  1244  GET              /api/recordings/session/<sid>                    api_recording_session   [nc/routes/recordings.py]
  1319  POST             /api/recordings/session/<sid>/join               api_recording_session_join   [nc/routes/recordings.py]
  1208  GET              /api/recordings/sessions                         api_recording_sessions   [nc/routes/recordings.py]
   812  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   708  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   486  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   464  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   505  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   522  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   574  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   440  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   265  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   165  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   596  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   413  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   134  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   535  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   561  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   191  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   216  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   388  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   134  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   144  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   475  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   465  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   500  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    65  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    86  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    52  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
   102  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   354  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
    92  GET              /api/selftest                                    api_selftest   [nc/routes/selbsttest.py]
   444  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
   128  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   219  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   214  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   274  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   110  GET              /api/storage                                     api_storage   [nc/routes/wartung.py]
   116  POST             /api/storage/cleanup                             api_storage_cleanup   [nc/routes/wartung.py]
   448  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   340  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   370  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
   126  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   273  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    88  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   298  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   230  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   254  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   185  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   150  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   210  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    56  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   206  GET              /api/summary/preview                             api_summary_preview   [nc/routes/auskunft.py]
    72  GET              /api/system                                      api_system   [nc/routes/systemlage.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   178  GET              /api/system/check_timing                         api_check_timing   [nc/routes/systemlage.py]
   117  GET              /api/system/config_drift                         api_config_drift   [nc/routes/systemlage.py]
   140  GET              /api/system/config_snapshot                      api_system_config_snapshot   [nc/routes/systemlage.py]
   238  GET              /api/system/preflight                            api_system_preflight   [nc/routes/systemlage.py]
   104  GET              /api/system/preflight_history                    api_system_preflight_history   [nc/routes/systemlage.py]
   370  GET              /api/system/resilience                           api_system_resilience   [nc/routes/systemlage.py]
   377  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
   176  GET              /api/top                                         api_top   [nc/routes/auskunft.py]
   238  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   453  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   482  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   402  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   415  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   511  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   388  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   263  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   308  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   332  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   319  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   165  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   277  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   135  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   369  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   424  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   252  GET              /api/trend-7d                                    api_trend_7d   [nc/routes/auskunft.py]
   121  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
   100  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   132  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   113  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   125  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    77  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
   101  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    55  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   453  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   419  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   478  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   458  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   441  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   434  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
   238  GET              /api/userstats                                   api_userstats   [nc/routes/auskunft.py]
   305  GET              /api/version                                     api_version   [nc/routes/auskunft.py]
    52  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    92  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   123  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
   107  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   131  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   152  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   164  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    89  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
   113  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    67  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   199  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
   382  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands in discordbot.py (60)

```
   803  /ai                     
  1207  /ask                    
   904  /assign_role            
   954  /ban                    
  2065  /botstats               
  1466  /clearwarns             
  2029  /clip                   
  2014  /clipoftheweek          
  1333  /clips                  
   859  /create_category        
   830  /create_channel         
   894  /create_group           
   869  /create_role            
   845  /create_voice           
  1090  /daily                  
  1236  /event                  
  1278  /events                 
  1376  /follow                 
  1361  /help                   
   944  /kick                   
  1065  /leaderboard            
  1320  /livenow                
  1348  /post_test              
  1168  /profile                
   976  /purge                  
  1052  /rank                   
  1308  /recstatus              
   914  /remove_role            
   816  /restream_status        
   924  /set_channel_perms      
  1019  /setup_community        
  1036  /setup_targets          
  1408  /stats                  
   733  /status                 
  1537  /streaminfo             
  2117  /sys_aireset            KI-Kontext zurücksetzen (TG: /aireset)
  2119  /sys_bulkadd            Mehrere User tracken (TG: /bulkadd a b c)
  2110  /sys_cleanup            Alte Aufnahmen aufräumen (TG: /cleanup)
  2121  /sys_cookies            Cookie-Status (TG: /cookies)
  2116  /sys_diag               Vollständige Diagnose (TG: /diag)
  2120  /sys_live               Live-Check erzwingen (TG: /live @user)
  2115  /sys_logs               Letzte Fehler-Logs (TG: /logs)
  2107  /sys_pause              Tracking pausieren (TG: /pause @user)
  2111  /sys_quota              Speicher-Quota (TG: /quota)
  1521  /sys_report             
  2112  /sys_res                System-Ressourcen (TG: /sysres)
  2108  /sys_resume             Tracking fortsetzen (TG: /resume @user)
  2109  /sys_stoprec            Aufnahme grazil stoppen (TG: /stoprec @user)
  2114  /sys_summary            Tageszusammenfassung (TG: /summary)
  2118  /sys_teststream         Recorder-Selbsttest (TG: /teststream)
  2113  /sys_topusers           Top-Streamer-Statistik (TG: /topusers)
  1498  /sys_unpause            
   964  /timeout                
  1476  /topstreamers           
   761  /track                  
   746  /tracklist              
  1390  /unfollow               
   793  /untrack                
  1429  /warn                   
  1452  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2274  on_member_join
  2236  on_message
  2143  on_raw_reaction_add
  2309  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    58-73     konfiguriere
    76-456    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (45 Funktionen)

```
  1614-1665   _award_xp
  1834-1863   _clip_week_leader
  1887-1901   _clipoftheweek_loop
  2425-2487   _community_events_loop
  1571-1593   _dc_client
  1596-1605   _dc_offen
  2527-2562   _disc_automod_check
   423-428    _disc_sprache_setzen
  1668-1716   _discord_ai_automod
   556-595    _discord_automod
  1719-1739   _discord_azrael_reply
  1904-2384   _discord_run_once
   258-316    _discord_start
   319-373    _ensure_discord_invite
  2390-2422   _ensure_error_channel
   444-457    _ensure_rank_roles
   692-706    _ensure_team_roles
  2490-2520   _error_channel_loop
   605-609    _guard
   525-553    _handle_voice_ai
   431-441    _is_admin
  1782-1793   _liveboard_loop
   612-630    _on_level_up
   521-522    _par_chat_id
  1866-1884   _post_clip_of_week
  1796-1814   _post_weekly_digest
   460-486    _provision_base_channels
   489-505    _provision_user_channels
  1300-1397   _reg_betrieb
   990-1079   _reg_community_setup
  1082-1157   _reg_daily_profil
  1200-1297   _reg_frage_events
   720-818    _reg_info
   936-987    _reg_moderation
  1160-1197   _reg_profil
   885-933    _reg_rollen
   821-882    _reg_server
  1400-1487   _reg_streamer
  1490-1568   _reg_system
   665-689    _run_tg_handler
   508-518    _tracked_usernames
   163-237    _uebernehmen
  1748-1779   _update_liveboard
  1817-1831   _weekly_digest_loop
   240-243    starte
```

## Top-Level-Symbole in bot.py (512 Funktionen, 2 Klassen)

```
 23945-23967  _abbruch_datenbank_unlesbar
  2639-2640   _abo_key
  2660-2678   _abo_probe_dump
 24018-24036  _abschluss
 15463-15470  _ad_allowlist
 16439-16445  _agent_for
 16448-16464  _ai_telemetry
 16959-16977  _alert
 20363-20413  _alert_monitor_loop
 20765-20827  _announce_loop
  3492-3502   _anthropic_key
  3509-3511   _anthropic_model
  9476-9479   _arg_int
  2631-2636   _as_dict
 23695-23704  _async_exc_handler
 17140-17162  _audio_tap_cmd
 17720-17779  _audio_tap_melden
 17176-17200  _audio_tap_sammler
 23970-24005  _aufraeumen
  9644-9713   _auth_cookie
  9611-9640   _auth_guard
  1868-1873   _auto_on
 18396-18414  _auto_restream_loop
 13373-13415  _avatar_frames_laden
 21845-21860  _azrael_broadcast_reply
 21745-21767  _azrael_chat_reply
 21717-21742  _azrael_chat_should_reply
 21773-21775  _azrael_gate_cfg
 16469-16483  _azrael_live_state
 19390-19404  _azrael_overlay_state
 16841-16895  _azrael_proactive_loop
 16287-16343  _azrael_reaction_to_chats
 21778-21785  _azrael_reply_all_chats
 21704-21714  _azrael_self_names
 21813-21842  _azrael_send_to
 13334-13370  _azrael_spricht
 16489-16510  _azrael_system
 20497-20500  _backup_active
 20578-20591  _backup_loop
 23768-23777  _brain_crowdsec_snap
 20284-20293  _brain_growth_loop
 10035-10062  _brain_growth_snapshot
  2573-2593   _brain_hint_delay
 23840-23875  _brain_moderation_snap
  6371-6399   _brain_notify
 23878-23900  _brain_recording_snap
 23780-23837  _brain_restream_health
 23903-23916  _brain_tiktok_status_snap
 11331-11348  _browser_push
  6411-6498   _build_daily_summary
 13694-13698  _build_restream_cmd
  5193-5220   _can_stop_tracking
  1981-2003   _capture_set_cookies
 12011-12014  _cfg_get
 12017-12019  _cfg_set
 19114-19149  _channel_set_all
 12562-12565  _chat_connected
 12568-12584  _chat_disconnected
  8537-8548   _chat_is_forum
 17527-17552  _chat_listener_abbauen
 12604-12606  _chat_sanitize
 12547-12559  _chat_stat
 12587-12590  _chat_stats_snapshot
  3795-3807   _check_ai_models_sync
 10317-10360  _classify_pool_anonymity
 10363-10380  _classify_pool_anonymity_bg
   864-886    _claude_chat_sync_metered
  9505-9512   _client_ip
 20911-20938  _clip_prune
 20941-20951  _clip_recfile_for
 21361-21367  _clip_should_velocity
 20992-21074  _clip_to_discord
  3688-3697   _close_ai_session
 21891-21906  _cohost_broadcast
 21876-21877  _cohost_cfg
 21932-21944  _cohost_fire_highlight
 21880-21888  _cohost_gate
 21909-21929  _cohost_highlight
  9965-9967   _conv_messages
  6770-6831   _cookie_alarm_loop
  2072-2077   _cookie_autofetch_info
  2055-2059   _cookie_autorefresh_info
  1958-1962   _cookie_header
  2089-2122   _cookies_selbst_holen
  4023-4035   _create_index_safe
 19836-19942  _crowdsec_status
 19782-19833  _crowdsec_via_lapi
 19686-19704  _cscli_bin
 19713-19726  _cscli_path
  6660-6685   _daily_summary_loop
 19744-19761  _darf_journal_lesen
  3056-3081   _darf_ytdlp_nachschlagen
 11512-11533  _dashboard_adresse
 20337-20360  _db_maintenance_loop
  6629-6657   _db_vacuum_loop
 15486-15510  _detect_foreign_ad
  1549-1560   _diag_path_owner
 16747-16791  _director_finalize
 17709-17716  _director_for
 16696-16744  _director_mark
 21226-21229  _disc_state_get
 21232-21239  _disc_state_set
 20265-20274  _discord_bot_starten
 20229-20240  _discord_einladung_merken
 20277-20281  _discord_invite
 20243-20262  _discord_kontext
 21187-21223  _discord_live_thread
 16898-16910  _discord_notify
 20201-20226  _discord_ops_alert
 21085-21183  _discord_post_user
 20830-20836  _discord_stop
  6688-6765   _disk_alarm_loop
 23383-23432  _disk_autoclean
 23550-23563  _disk_guard_loop
 13312-13319  _drossel_hoeher
 13308-13309  _drossel_stufe
 13322-13330  _drossel_zuruecksetzen
 11689-11691  _dump_all_threads
 10243-10306  _enrich_proxies_with_geo
  2151-2212   _ensure_cookie_file_netscape
  8596-8599   _ensure_notify_topic
 10487-10524  _ensure_proxy_ready
  8550-8577   _ensure_topic
   713-715    _env_int
   718-720    _env_int_range
 16943-16956  _event_webhook
 12362-12375  _evolution_loop
  5813-5847   _extract_file_payload
  2284-2286   _extract_urls_from_streamurl_node
 19729-19736  _f2b_sudo_hint
 24039-24102  _fatal_vom_botteil
  4657-4667   _fehler_text
 10144-10162  _fetch_proxy_list
 17496-17524  _fetch_tiktok_room_id
   796-799    _ff_cmd
 13141-13146  _find_chromium
  3412-3414   _find_external_recorder
  2289-2291   _find_stream_urls
 12062-12087  _fire_webhooks
  7597-7606   _fork_safe
   897-910    _freeai_chat_sync_metered
 19775-19779  _geo_lookup_ips
  3676-3685   _get_ai_session
  7430-7470   _get_live_info
  2905-2912   _get_resolve_semaphore
  7879-8251   _handle_single_tracking
 23205-23207  _hb
 23210-23227  _hb_while
 12618-12620  _highlight_cfg
 12623-12652  _highlight_observe
 13149-13167  _htmlov_screenshot_cmd
 17202-17212  _httpx_proxy
 12095-12107  _in_quiet_hours
 23931-23942  _init_db_oder_abbruch
 24654-24685  _install_fast_eventloop
  9371-9425   _install_fast_json
 11694-11710  _install_faulthandler
 18442-18451  _intel_ensure_schema
 18489-18524  _intel_index_loop
 18463-18473  _intel_index_one
 18454-18460  _intel_semantic
  5182-5191   _is_authorized
  7780-7786   _is_dead
  2274-2276   _is_hevc
 19764-19766  _is_private_ip
  1767-1774   _is_process_running
  6401-6408   _is_quiet_hours
  1342-1351   _is_upload_window
  4522-4537   _iso
  9460-9473   _json_error_handler
  6623-6624   _kick_broadcaster_id
  6535-6577   _kick_follower_count
  6519-6522   _kick_slug
 11144-11151  _kick_user_token
 23919-23928  _kickmod_boot
  4112-4115   _kind_from_filename
 12124-12126  _latest_popularity
  1704-1713   _laufstand
 23513-23547  _laufstand_loop
 18105-18154  _live_react_loop
 17782-18094  _live_react_worker
 16346-16357  _live_transcript_push
 18096-18103  _live_users
 16794-16838  _living_title_loop
 20503-20575  _local_backup_scan
  9442-9456   _log_5xx
   786-793    _log_sicher
 13706-13718  _looks_like_codec_err
 13701-13703  _looks_like_source_expired
  7647-7677   _loop_fehler
 11714-11723  _loop_heartbeat
 23175-23202  _loop_lag_monitor
 11726-11794  _loop_watchdog_thread
 16226-16240  _loyalty_add
 16217-16223  _loyalty_get
 16243-16251  _loyalty_top
 12234-12236  _manual_donations_total
  4864-4883   _manual_status
  7788-7789   _mark_dead
 10763-10779  _marketing_loop
 21792-21810  _maybe_handle_command
 23649-23673  _maybe_hype_clip
 20880-20908  _meme_klassifizieren
  3990-4013   _migrate_columns
 22071-22082  _mod_is_exempt
 22085-22090  _mod_warn_first
 22093-22096  _mod_warn_text
 12402-12410  _modlog
  1042-1044   _multistream_targets
  3084-3120   _nachschlag_ytdlp
  7609-7610   _nc_create_subprocess_exec
  7613-7614   _nc_create_subprocess_shell
 11081-11098  _news_loop
 12429-12431  _normalize_ingest
  2504-2521   _note_check_duration
  8590-8593   _notify_topic_name
  3123-3143   _ohne_url_melden
 16372-16380  _oracle_memories
 16645-16679  _oracle_memorize
 16383-16396  _oracle_persona
 16365-16369  _oracle_recent_text
 12775-12776  _ov_atomic_write
 12766-12768  _ov_bar
 15389-15401  _ov_clip_text
 12771-12772  _ov_oneline
 19441-19470  _overlay_push
 13095-13138  _overlay_render_size
 12498-12502  _overlay_session_reset
 19406-19408  _overlay_src_ok
 15473-15483  _own_invites
 13090-13092  _parse_size
 19950-20030  _parse_ssh_attacks
  7032-7065   _pause_resume_cmd
  2009-2053   _persist_refreshed_cookies
  1912-1944   _pick_checked_pull_proxy
  9541-9554   _pin_auth_value
  9600-9601   _pin_clear_fail
  9580-9583   _pin_locked
  9586-9597   _pin_note_fail
  9557-9577   _pin_ok
 19250-19275  _piper_pick_model
 19335-19384  _piper_say
 12024-12059  _post_json_threaded
 13069-13087  _probe_video_size
  1795-1812   _proc_is_recorder
 10456-10484  _proxy_pool_refresh_loop
  1878-1909   _proxy_report_recording
 11679-11681  _prune_stall_dumps
 10833-11003  _public_stats
  2080-2086   _pull_proxy_still
 16914-16940  _push_notify
  9760-9762   _pwa_dir
 10213-10228  _quick_validate_proxy
 12090-12092  _quiet_hours_config
  9725-9758   _rate_guard
 16187-16193  _react_warn
  7517-7556   _reap_proc
  8820-8887   _rec_auto_abschalten
  8767-8817   _rec_frueh_getrennt
  8654-8712   _rec_kategorie_melden
  8715-8764   _rec_totstreak_fortschreiben
  2544-2566   _record_check_outcome
   781-783    _redact_stream_urls
 10383-10453  _refresh_proxy_pool
  2321-2412   _resolve_via_html
  2685-2882   _resolve_via_webcast_api_v2
  2945-3032   _resolve_via_ytdlp
 21401-21530  _resolve_youtube_ingest
  2300-2318   _resolver_stumm
 12481-12492  _restream_active_sources
 13418-13542  _restream_avatar_feeder_start
 13545-13554  _restream_avatar_feeder_stop
 17555-17673  _restream_chat_guardian
 12655-12727  _restream_chat_push
 12752-12761  _restream_chat_push_async
 13170-13279  _restream_html_overlay_start
 13282-13295  _restream_html_overlay_stop
 12440-12463  _restream_overlay_files
 18158-18190  _restream_platform_state
 18358-18393  _restream_resume_after_restart
 13602-13660  _restream_tts_enqueue_wav
 13031-13063  _restream_tts_feeder
 13028-13029  _restream_tts_fifo_path
 13557-13584  _restream_tts_start
 13586-13600  _restream_tts_stop
 18196-18355  _restream_verify_loop
 20468-20480  _retention_loop
 20462-20465  _retention_scan
  2642-2644   _room_is_abo
  5851-5968   _run_ai_call
 11817-11830  _run_async_from_flask
 19769-19772  _run_priv
 24642-24650  _run_selfcheck_and_exit
 20483-20494  _s3_client
  7815-7866   _safe_send
  4790-4806   _sample_net_throughput
  2596-2617   _schedule_next_check
 20416-20459  _scheduler_loop
  4016-4020   _schema_pk
 11834-11839  _scraper_session
 22099-22138  _screen_full
 11195-11232  _sec_headers
  2279-2281   _select_stream_from_data_section
 24392-24639  _selfcheck
  8602-8636   _send_live_notice
  1365-1369   _should_defer_upload
 20954-20989  _shrink_for_discord
  9765-9777   _sicheres_ziel
 20296-20334  _sicherheits_erinnerung_loop
 23570-23587  _sign_health_check
 23590-23609  _sign_health_loop
  4540-4565   _sitzung_bestimmen
  7626-7637   _spawn
 25060-25090  _spawn_from_flask
 17214-17493  _start_chat_listener
 11797-11814  _start_loop_watchdog
 11030-11076  _stats_loop
 11009-11012  _stats_output_path
 11015-11027  _stats_write
 19287-19301  _stimme_saubern
 19308-19332  _stimme_schon_gesagt
  8330-8346   _storage_cleanup_loop
 23629-23636  _story_for
  3437-3443   _stream_url_expiry
  3445-3450   _stream_url_ttl
 15436-15443  _streamer_persona_get
 20600-20722  _system_backup
 20731-20761  _system_backup_loop
 11639-11657  _task_auf_bot_schleife
  7680-7726   _telegram_polling_fehler
 10165-10204  _test_proxy
 10711-10727  _testpush_resolve_live
  7791-7812   _tg_sprache_setzen
  8509-8519   _tg_topics_load_into_mem
  8506-8507   _tg_topics_path
  8521-8528   _tg_topics_save
  9515-9523   _token_ok
  8531-8535   _topic_forget
 12110-12121  _tracking_max_duration
  4320-4334   _tracking_remove_cleanup
  4351-4363   _tracking_resume_cleanup
  1607-1630   _try_attach_file_handler
 19277-19285  _tts_cleanup
 10687-10691  _tunnel_effective
 23435-23455  _tunnel_lage
 23458-23510  _tunnel_wacht_loop
 18773-18826  _twitch_channel_status
 22141-22286  _twitch_chat_loop
 21245-21258  _twitch_clip_versuchen
 21955-22058  _twitch_eventsub_loop
  1388-1401   _upload_queue_add
  1412-1414   _upload_queue_count
  1371-1380   _upload_queue_load
  1361-1363   _upload_queue_path
  1403-1410   _upload_queue_remove
  1382-1386   _upload_queue_save
  1416-1457   _upload_window_loop
  7490-7497   _uptime_s
 12417-12426  _url_host
  3146-3240   _url_nachschlag
   857-861    _usage_record_claude
 23743-23765  _v37_pause_source
 23707-23717  _v37_restream_restart
 23720-23740  _v37_unpause_source
  7729-7773   _verbindung_verloren
  6580-6611   _viewer_sample_loop
  9604-9607   _wants_html
  7500-7514   _warn_empty_env
 23248-23369  _watchdog_loop
 21676-21684  _wchat_thank_ok
 16982-17012  _whisper_get_model
  7587-7594   _whisper_native_section
 16174-16180  _whisper_pool
 17106-17138  _whisper_segments
 17014-17030  _whisper_stumm
 17033-17103  _whisper_transcribe
 12823-12985  _write_restream_overlay
 12785-12820  _write_restream_overlay_async
 22310-22406  _youtube_api_chat_loop
 18829-18932  _youtube_api_status
 18935-19002  _youtube_channel_status
 22409-22570  _youtube_chat_loop
 21261-21286  _youtube_clip_versuchen
 21536-21549  _youtube_restream_autoconfig
 21552-21576  _youtube_restream_autoconfig_inner
 21643-21671  _youtube_send
 19070-19111  _youtube_set_channel
 21579-21613  _yt_access_token
 21616-21631  _yt_live_chat_id
 21639-21640  _yt_sendrate_cfg
 22289-22304  _yt_timeout
  2929-2930   _ytdlp_detect_available
  2932-2943   _ytdlp_note_result
 11684-11686  _zombie_child_count
  7366-7390   about
  4231-4235   add_ai_log_entry
  4148-4151   add_archive_entry
  4828-4830   add_archive_rule
  4568-4639   add_recording
  4295-4312   add_tracking
  5971-6004   ai
  3821-3894   ai_chat
  3928-3938   ai_history_append
  3940-3945   ai_history_clear
  3917-3926   ai_history_load
  3902-3915   ai_rate_limit_check
  6033-6041   aireset
 16513-16532  azrael_chat
 22575-22697  brain_cmd
  3453-3458   build_recording_cmd
  4315-4318   bulk_add_trackings
  6834-6893   bulkadd
  8349-8489   check_all_trackings
  4367-4379   claim_live_transition
 15513-16106  class KickModerator
 13721-15276  class RestreamManager
 10570-10612  classify_proxy_anonymity
  6079-6277   cleanup
  5118-5124   cleanup_old_recordings
  4513-4520   clear_recording
 21289-21358  clip_moment
  4780-4783   compute_storage_forecast
  6956-7029   cookies_cmd
  4286-4292   count_trackings_for_chat
  4218-4229   decide_preferred_recorder
  4158-4161   delete_archive_entry
  4832-4834   delete_archive_rule
  5508-5655   diag
 22809-22870  einnahmen_cmd
  4774-4777   find_recordings_by_fingerprint
  4179-4195   finish_recording_attempt
  4339-4341   get_all_active_trackings
  4246-4248   get_all_checks
  4641-4644   get_all_recordings
  4723-4725   get_all_tags_with_counts
  4751-4754   get_annotations_for_recording
  4153-4156   get_archive_entry
  4744-4747   get_bookmarked_recordings
  2139-2144   get_cookie_health
  4711-4717   get_event_log
  4202-4216   get_last_recording_attempt
  3243-3374   get_live_status
  5057-5060   get_manual_recordings
  4759-4762   get_or_compute_inspect_sync
  5159-5162   get_outcome_breakdown
  4730-4733   get_priority_poll_interval
  4197-4200   get_recent_recording_attempts
  4646-4649   get_recording_by_id
  4737-4740   get_recording_note
  3622-3645   get_redis
  4275-4278   get_stats
  5112-5116   get_storage_stats
  4852-4854   get_tiktok_status_distribution
  4381-4390   get_tracking_state
  4336-4337   get_trackings_for_group
  5073-5076   get_trash_recordings
  8890-9350   handle_recording_finished
  4043-4103   init_db
  4824-4826   list_archive_rules
  5312-5350   live
  7869-7877   live_check_worker
  3700-3734   llm_chat
  3757-3785   llm_chat_sync
  3742-3754   llm_list_models
  4670-4703   log_event
  1729-1762   log_recording_failure
  7179-7228   logs_cmd
 24105-24382  main
  6007-6030   on_ai_media
  7305-7331   on_ai_reply
  7334-7363   on_azrael_mention
  7395-7425   on_callback
 16538-16642  oracle_handle
  7068-7071   pause_tracking
  5172-5177   profile_keyboard
  7130-7176   quota
  8253-8327   reaper_loop
  4848-4850   record_tiktok_status
  6046-6076   recstatus
  3647-3655   redis_get_json
  3658-3664   redis_set_json
 22873-22883  report_cmd
 10615-10617  report_proxy_result
  2415-2457   resolve_tiktok_live_stream
  5068-5071   restore_recording
  7074-7077   resume_tracking
  4837-4842   run_archive_rules
 22886-23155  run_bot
 11536-11630  run_flask
  4812-4815   sample_bandwidth_for_active
  4238-4244   save_tiktok_check
  4505-4511   set_recording_file
  4344-4348   set_tracking_paused
  5063-5066   soft_delete_recording
  8642-8652   split_and_send_video
  5225-5267   start
  4163-4177   start_recording_attempt
  6280-6318   stats
  5002-5055   stop_manual_recording
  7080-7127   stoprec
  6504-6512   summary_cmd
  7231-7302   sysres
  5657-5801   teststream
  5269-5310   tiktok
  6896-6953   topusers
  5387-5444   track
  5352-5384   track_exact
  5458-5506   tracklist
  4886-5000   trigger_manual_recording
  4466-4503   try_acquire_recording_lock
  5079-5081   universal_search
  5446-5456   untrack
 22700-22806  update_cmd
  4769-4772   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, class BestandUnbekannt, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, finde_ohne_eintrag, get_archive_entries_paged, get_archive_entry, run_archive_file_check, uebernehmen
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            config, configure
audiotap.py            diagnose, melden, warum_kein_tap
aufnahmefolge.py       aufnahme_geglueckt, daten_geflossen, melden_erlaubt, nach_403, nach_frueher_trennung, nach_totem_versuch, sitzung_zuende, sperre_rest
aufnahmekategorie.py   kategorisiere
aufnahmesitzung.py     abdeckung, concat_cmd, concat_liste, gehoert_dazu, luecken, sekunden, sitzung_id, zieldatei
auslieferung.py        schreibe, stand, text
avatarloop.py          blinzeln, ruhe_seit, schleife, zustand
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, fehlgrund, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_region, s3_zugang, sys_backup, sys_hour, sys_keep, sys_max_file_mb
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
binresolve.py          resolve
botctx.py              class BotKontext
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatfolge.py           entscheide
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           anzeigename, configure, darf_pingen, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, rollen_id, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookieholen.py         aktualisiere, aus_browser, configure, hole_gastcookies, schreibe, zusammenfuehren
cookies.py             configure, gesundheit, lade_jar, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, erwartete_namen, fehlende_namen, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            erlaubt_offen, geschuetzt, host, lage, nur_lokal, offen_im_netz, zurueckgefallen
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbrestore.py           archive, dump_aus_archiv, einsetzen, einspielen, vorbereiten
dbwrap.py              class DatenbankUnlesbar, configure_db, datei_diagnose, db_async, db_conn, get_pool, set_pool
ddlsafe.py             ddl, ist_schon_da
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
discordrang.py         rang_fuer_level, slug, xp_fuer_level, xp_zu_level
discordstate.py        invite, state_get
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventlog.py            leeren, schreibe, stand
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
fehlertext.py          nach_aussen, saeubern
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      avatar_kette, chat_umbruch_w, chat_zeilen, drawtext_chain, studio_chain, studio_masse
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, dienstmeldung, katalog_kennt, last_errors, list_models_sync, stream_haeppchen, stream_rest
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
highlights.py          check, new_state, observe, score, zustand
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, configure, oauth_exchange, search_category, send_message, slug, timeout_user, update_channel, user_token
laufstand.py           befehl, veraltet, vergleich
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
livecache.py           aufraeumen, frisch, holen, setzen
livefolge.py           braucht_url_nachschlag, hat_stream_url, live_gesehen, offline_bestaetigt, poll_abstand, ruhezeit
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             fuer_log, redact_cookie_zeilen, redact_pull_urls, redact_stream_urls, url_ohne_zugang
logschleuse.py         class Schleuse, entkoppeln, stoppen, verloren, wartend, zuruecksetzen
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
meldetakt.py           melden, zuruecksetzen, zusatz
memeklip.py            class Fenster, frage, lies_urteil, soll_clippen
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modki.py               frage, lies_klassifikation, lies_schimpfwoerter
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
outcomes.py            get_outcome_breakdown
overlaytext.py         configure, latest_popularity, ov_atomic_write, ov_bar, ov_oneline, overlay_src_ok
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
reccmd.py              build_recording_cmd, configure
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
resolvergrund.py       http_grund, quelle_lage, quelle_laut, text
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, fenstergroesse, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamcmd.py         build, configure, drossel_avatar_aus, drossel_bitrate, drossel_canvas, drossel_fps, drossel_preset, drossel_zusatz, schriftart
restreamgesundheit.py  blind_markieren, frische_tee_fehler, marke_setzen
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              create_schema
schemastand.py         lege_an, lies, pruefe, schreibe, streng
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sicherpfad.py          pruefe_unter, sicher_join, sicherer_name, unter
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             cleanup, forecast, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
systemprobe.py         active_recorder, ai_alive, ai_calls_total, cache_leeren, cached_probe, configure, cpu_load_snapshot, disk_pct, recorder_pref, recordings_dir, redis_alive, redis_url, redis_version
telegramfehler.py      dauer_text, grund, ist_fehler, text, zuruecksetzen
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
tonspur.py             class Fehlschlag, hat_ton, hat_tonspur, ist_tonlos_fehler, nachruest_cmd, pruef_cmd, pruefen, sichern, stille_eingabe
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
tunnelwacht.py         lage, meldung, probe, probe_cmd
twitchoauth.py         access_token, authorize_url, configure, create_clip, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
webserver.py           bindung, ist_loopback, schema, threads, tls_lage, waehle
whispercfg.py          geladen, name, verfuegbar, waehle
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytdlpurl.py            urls_aus_json
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status, upload_clip
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
