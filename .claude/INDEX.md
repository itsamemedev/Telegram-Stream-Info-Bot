# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
  9841  GET              /                                                dashboard
 11888  GET              /api/abo/status                                  api_abo_status
 11842  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 10629  GET              /api/automation/status                           api_automation_status
 10651  POST             /api/automation/toggle                           api_automation_toggle
 19177  GET              /api/channel/categories                          api_channel_categories
 19183  POST             /api/channel/set                                 api_channel_set
 19030  GET              /api/channels/status                             api_channels_status
 18704  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 18687  GET              /api/clips                                       api_clips
 18733  POST/DELETE      /api/clips/clear                                 api_clips_clear
 18612  GET              /api/debug/threads                               api_debug_threads
 11853  GET              /api/events                                      api_events
 11337  GET              /api/events/stream                               api_events_stream
 11164  GET              /api/health                                      api_health
 18646  POST             /api/highlights/config                           api_highlights_config
  9775  POST             /api/login                                       dashboard_login_submit
 12178  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11252  GET              /api/notify/status                               api_notify_status
 11263  POST             /api/notify/test                                 api_notify_test
 11942  GET              /api/proxy/heatmap                               api_proxy_heatmap
 11919  GET              /api/proxy/trend                                 api_proxy_trend
 18753  GET              /api/tts/<fn>                                    api_tts_file
 19528  GET              /api/upload_window                               api_upload_window
 11454  GET              /archive/<int:eid>/download                      archive_download
 11482  GET              /download/<int:recording_id>                     download
 11411  GET              /health                                          health
 18558  GET              /healthz                                         healthz
  9766  GET              /login                                           dashboard_login_page
  9796  GET              /logout                                          dashboard_logout
  9803  GET              /manifest.webmanifest                            pwa_manifest
 19501  GET              /overlay                                         overlay_page
  9827  GET              /pwa-icon-<variant>.png                          pwa_icon
  9813  GET              /sw.js                                           pwa_service_worker
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
   433  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   418  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   238  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   195  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    73  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    80  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   485  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   259  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   286  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   379  POST             /api/db/restore/apply                            api_db_restore_apply   [nc/routes/settings.py]
   323  GET              /api/db/restore/list                             api_db_restore_list   [nc/routes/settings.py]
   341  POST             /api/db/restore/prepare                          api_db_restore_prepare   [nc/routes/settings.py]
   246  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
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
   474  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   464  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   499  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
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

## Discord-Slash-Commands in discordbot.py (65)

```
  2080  /about                  Ueber diesen Bot
   809  /ai                     
  2080  /aireset                KI-Kontext zuruecksetzen
  1213  /ask                    
   910  /assign_role            
   960  /ban                    
  2035  /botstats               
  2080  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2080  /bulkadd                Mehrere User auf einmal tracken · a b c
  2080  /cleanup                Alte Aufnahmen aufraeumen
  1468  /clearwarns             
  1999  /clip                   
  1984  /clipoftheweek          
  1339  /clips                  
  2080  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
   865  /create_category        
   836  /create_channel         
   900  /create_group           
   875  /create_role            
   851  /create_voice           
  1096  /daily                  
  2080  /diag                   Vollstaendige Diagnose
  2080  /einnahmen              Einnahmen und Spenden
  1242  /event                  
  1284  /events                 
  1378  /follow                 
  1367  /help                   
   950  /kick                   
  1071  /leaderboard            
  2080  /live                   Live-Status sofort pruefen · @user
  1326  /livenow                
  2080  /logs                   Letzte Fehler aus dem Log
  2080  /pause                  Tracking pausieren · @user
  1354  /post_test              
  1174  /profile                
   982  /purge                  
  2080  /quota                  Speicher-Quota
  1058  /rank                   
  1314  /recstatus              
   920  /remove_role            
  2080  /report                 Azrael-Sentinel-Wochenreport
   822  /restream_status        
  2080  /resume                 Tracking fortsetzen · @user
   930  /set_channel_perms      
  1025  /setup_community        
  1042  /setup_targets          
  1410  /stats                  
   781  /status                 
  2080  /stoprec                Laufende Aufnahme sauber beenden · @user
  1506  /streaminfo             
  2080  /summary                Tageszusammenfassung
  2080  /sysres                 System-Ressourcen
  2080  /teststream             Recorder-Selbsttest · @user
  2080  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
   970  /timeout                
  1478  /topstreamers           
  2080  /topusers               Top-Streamer nach Aufnahmen
   711  /track                  
  2080  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   794  /tracklist              
  1392  /unfollow               
  2080  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   743  /untrack                
  1431  /warn                   
  1454  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2238  on_member_join
  2200  on_message
  2101  on_raw_reaction_add
  2273  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    58-73     konfiguriere
    76-456    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (46 Funktionen)

```
  1583-1634   _award_xp
  1803-1832   _clip_week_leader
  1856-1870   _clipoftheweek_loop
  2389-2451   _community_events_loop
  1540-1562   _dc_client
  1565-1574   _dc_offen
  2491-2526   _disc_automod_check
   401-406    _disc_sprache_setzen
  1637-1685   _discord_ai_automod
   534-573    _discord_automod
  1688-1708   _discord_azrael_reply
  1873-2348   _discord_run_once
   236-294    _discord_start
   297-351    _ensure_discord_invite
  2354-2386   _ensure_error_channel
   422-435    _ensure_rank_roles
   674-688    _ensure_team_roles
  2454-2484   _error_channel_loop
   583-587    _guard
   503-531    _handle_voice_ai
   409-419    _is_admin
  1751-1762   _liveboard_loop
   590-608    _on_level_up
   499-500    _par_chat_id
  1835-1853   _post_clip_of_week
  1765-1783   _post_weekly_digest
   438-464    _provision_base_channels
   467-483    _provision_user_channels
  1306-1399   _reg_betrieb
   996-1085   _reg_community_setup
  1088-1163   _reg_daily_profil
  1206-1303   _reg_frage_events
   768-824    _reg_info
   942-993    _reg_moderation
  1166-1203   _reg_profil
   891-939    _reg_rollen
   827-888    _reg_server
  1402-1489   _reg_streamer
  1492-1537   _reg_system
   702-765    _reg_tracking
   643-671    _run_tg_handler
   486-496    _tracked_usernames
   153-215    _uebernehmen
  1717-1748   _update_liveboard
  1786-1800   _weekly_digest_loop
   218-221    starte
```

## Top-Level-Symbole in bot.py (517 Funktionen, 2 Klassen)

```
 24067-24089  _abbruch_datenbank_unlesbar
  2620-2621   _abo_key
  2641-2659   _abo_probe_dump
 24140-24158  _abschluss
 15487-15494  _ad_allowlist
 16463-16469  _agent_for
 16472-16488  _ai_telemetry
 16983-17001  _alert
 20388-20438  _alert_monitor_loop
 20790-20852  _announce_loop
  3473-3483   _anthropic_key
  3490-3492   _anthropic_model
  9461-9464   _arg_int
  2612-2617   _as_dict
 23817-23826  _async_exc_handler
 17164-17186  _audio_tap_cmd
 17744-17803  _audio_tap_melden
 17200-17224  _audio_tap_sammler
 24092-24127  _aufraeumen
  9629-9698   _auth_cookie
  9596-9625   _auth_guard
  1871-1876   _auto_on
 18420-18438  _auto_restream_loop
 13358-13400  _avatar_frames_laden
 21870-21885  _azrael_broadcast_reply
 21770-21792  _azrael_chat_reply
 21742-21767  _azrael_chat_should_reply
 21798-21800  _azrael_gate_cfg
 16493-16507  _azrael_live_state
 19414-19428  _azrael_overlay_state
 16865-16919  _azrael_proactive_loop
 16311-16367  _azrael_reaction_to_chats
 21803-21810  _azrael_reply_all_chats
 21729-21739  _azrael_self_names
 21838-21867  _azrael_send_to
 13319-13355  _azrael_spricht
 16513-16534  _azrael_system
 20522-20525  _backup_active
 20603-20616  _backup_loop
 23890-23899  _brain_crowdsec_snap
 20309-20318  _brain_growth_loop
 10020-10047  _brain_growth_snapshot
  2554-2574   _brain_hint_delay
 23962-23997  _brain_moderation_snap
  6352-6380   _brain_notify
 24000-24022  _brain_recording_snap
 23902-23959  _brain_restream_health
 24025-24038  _brain_tiktok_status_snap
 11316-11333  _browser_push
  6392-6479   _build_daily_summary
 13679-13683  _build_restream_cmd
  5174-5201   _can_stop_tracking
  1984-2006   _capture_set_cookies
 11996-11999  _cfg_get
 12002-12004  _cfg_set
 19138-19173  _channel_set_all
 12547-12550  _chat_connected
 12553-12569  _chat_disconnected
  8518-8529   _chat_is_forum
 17551-17576  _chat_listener_abbauen
 12589-12591  _chat_sanitize
 12532-12544  _chat_stat
 12572-12575  _chat_stats_snapshot
  3776-3788   _check_ai_models_sync
 10302-10345  _classify_pool_anonymity
 10348-10365  _classify_pool_anonymity_bg
   867-889    _claude_chat_sync_metered
  9490-9497   _client_ip
 20936-20963  _clip_prune
 20966-20976  _clip_recfile_for
 21386-21392  _clip_should_velocity
 21017-21099  _clip_to_discord
  3669-3678   _close_ai_session
 21916-21931  _cohost_broadcast
 21901-21902  _cohost_cfg
 21957-21969  _cohost_fire_highlight
 21905-21913  _cohost_gate
 21934-21954  _cohost_highlight
  9950-9952   _conv_messages
  6751-6812   _cookie_alarm_loop
  2074-2075   _cookie_autofetch_info
  2058-2062   _cookie_autorefresh_info
 23527-23549  _cookie_bezug_loop
 23552-23577  _cookie_bezug_runde
  1961-1965   _cookie_header
  2087-2101   _cookies_selbst_holen
  4004-4016   _create_index_safe
 19860-19966  _crowdsec_status
 19806-19857  _crowdsec_via_lapi
 19710-19728  _cscli_bin
 19737-19750  _cscli_path
  6641-6666   _daily_summary_loop
 19768-19785  _darf_journal_lesen
  3037-3062   _darf_ytdlp_nachschlagen
 11497-11518  _dashboard_adresse
 20362-20385  _db_maintenance_loop
  6610-6638   _db_vacuum_loop
 15510-15534  _detect_foreign_ad
  1552-1563   _diag_path_owner
 16771-16815  _director_finalize
 17733-17740  _director_for
 16720-16768  _director_mark
 21251-21254  _disc_state_get
 21257-21264  _disc_state_set
 20290-20299  _discord_bot_starten
 20253-20264  _discord_einladung_merken
 20302-20306  _discord_invite
 20267-20287  _discord_kontext
 21212-21248  _discord_live_thread
 16922-16934  _discord_notify
 20225-20250  _discord_ops_alert
 21110-21208  _discord_post_user
 20855-20861  _discord_stop
  6669-6746   _disk_alarm_loop
 23452-23501  _disk_autoclean
 23672-23685  _disk_guard_loop
 13297-13304  _drossel_hoeher
 13293-13294  _drossel_stufe
 13307-13315  _drossel_zuruecksetzen
 11674-11676  _dump_all_threads
 10228-10291  _enrich_proxies_with_geo
  2130-2191   _ensure_cookie_file_netscape
  8577-8580   _ensure_notify_topic
 10472-10509  _ensure_proxy_ready
  8531-8558   _ensure_topic
   716-718    _env_int
   721-723    _env_int_range
 16967-16980  _event_webhook
 12347-12360  _evolution_loop
  5794-5828   _extract_file_payload
  2263-2265   _extract_urls_from_streamurl_node
 19753-19760  _f2b_sudo_hint
 24161-24224  _fatal_vom_botteil
  4638-4648   _fehler_text
 10129-10147  _fetch_proxy_list
 17520-17548  _fetch_tiktok_room_id
   799-802    _ff_cmd
 13126-13131  _find_chromium
  3393-3395   _find_external_recorder
  2268-2270   _find_stream_urls
 12047-12072  _fire_webhooks
  7578-7587   _fork_safe
   900-913    _freeai_chat_sync_metered
 19799-19803  _geo_lookup_ips
  3657-3666   _get_ai_session
  7411-7451   _get_live_info
  2886-2893   _get_resolve_semaphore
  7860-8232   _handle_single_tracking
 23274-23276  _hb
 23279-23296  _hb_while
 12603-12605  _highlight_cfg
 12608-12637  _highlight_observe
 13134-13152  _htmlov_screenshot_cmd
 17226-17236  _httpx_proxy
 12080-12092  _in_quiet_hours
 24053-24064  _init_db_oder_abbruch
 24776-24807  _install_fast_eventloop
  9356-9410   _install_fast_json
 11679-11695  _install_faulthandler
 18466-18475  _intel_ensure_schema
 18513-18548  _intel_index_loop
 18487-18497  _intel_index_one
 18478-18484  _intel_semantic
  5163-5172   _is_authorized
  7761-7767   _is_dead
  2253-2255   _is_hevc
 19788-19790  _is_private_ip
  1770-1777   _is_process_running
  6382-6389   _is_quiet_hours
  1345-1354   _is_upload_window
  4503-4518   _iso
  9445-9458   _json_error_handler
  6604-6605   _kick_broadcaster_id
  6516-6558   _kick_follower_count
  6500-6503   _kick_slug
 11129-11136  _kick_user_token
 24041-24050  _kickmod_boot
  4093-4096   _kind_from_filename
 12109-12111  _latest_popularity
  1707-1716   _laufstand
 23635-23669  _laufstand_loop
 18129-18178  _live_react_loop
 17806-18118  _live_react_worker
 16370-16381  _live_transcript_push
 18120-18127  _live_users
 16818-16862  _living_title_loop
 20528-20600  _local_backup_scan
  9427-9441   _log_5xx
   789-796    _log_sicher
 13691-13703  _looks_like_codec_err
 13686-13688  _looks_like_source_expired
  7628-7658   _loop_fehler
 11699-11708  _loop_heartbeat
 23244-23271  _loop_lag_monitor
 11711-11779  _loop_watchdog_thread
 16250-16264  _loyalty_add
 16241-16247  _loyalty_get
 16267-16275  _loyalty_top
 12219-12221  _manual_donations_total
  4845-4864   _manual_status
  7769-7770   _mark_dead
 10748-10764  _marketing_loop
 21817-21835  _maybe_handle_command
 23771-23795  _maybe_hype_clip
 20905-20933  _meme_klassifizieren
  3971-3994   _migrate_columns
 22096-22107  _mod_is_exempt
 22110-22115  _mod_warn_first
 22118-22121  _mod_warn_text
 12387-12395  _modlog
  1045-1047   _multistream_targets
  3065-3101   _nachschlag_ytdlp
  7590-7591   _nc_create_subprocess_exec
  7594-7595   _nc_create_subprocess_shell
 11066-11083  _news_loop
 12414-12416  _normalize_ingest
  2485-2502   _note_check_duration
  8571-8574   _notify_topic_name
  3104-3124   _ohne_url_melden
 16396-16404  _oracle_memories
 16669-16703  _oracle_memorize
 16407-16420  _oracle_persona
 16389-16393  _oracle_recent_text
 12760-12761  _ov_atomic_write
 12751-12753  _ov_bar
 15413-15425  _ov_clip_text
 12756-12757  _ov_oneline
 19465-19494  _overlay_push
 13080-13123  _overlay_render_size
 12483-12487  _overlay_session_reset
 19430-19432  _overlay_src_ok
 15497-15507  _own_invites
 13075-13077  _parse_size
 19974-20054  _parse_ssh_attacks
  7013-7046   _pause_resume_cmd
  2012-2056   _persist_refreshed_cookies
  1915-1947   _pick_checked_pull_proxy
  9526-9539   _pin_auth_value
  9585-9586   _pin_clear_fail
  9565-9568   _pin_locked
  9571-9582   _pin_note_fail
  9542-9562   _pin_ok
 19274-19299  _piper_pick_model
 19359-19408  _piper_say
 12009-12044  _post_json_threaded
 13054-13072  _probe_video_size
  1798-1815   _proc_is_recorder
 10441-10469  _proxy_pool_refresh_loop
  1881-1912   _proxy_report_recording
 11664-11666  _prune_stall_dumps
 10818-10988  _public_stats
  2078-2084   _pull_proxy_still
 16938-16964  _push_notify
  9745-9747   _pwa_dir
 10198-10213  _quick_validate_proxy
 12075-12077  _quiet_hours_config
  9710-9743   _rate_guard
 16211-16217  _react_warn
  7498-7537   _reap_proc
  8805-8872   _rec_auto_abschalten
  8752-8802   _rec_frueh_getrennt
  8635-8697   _rec_kategorie_melden
  8700-8749   _rec_totstreak_fortschreiben
  2525-2547   _record_check_outcome
   784-786    _redact_stream_urls
 10368-10438  _refresh_proxy_pool
  2302-2393   _resolve_via_html
  2666-2863   _resolve_via_webcast_api_v2
  2926-3013   _resolve_via_ytdlp
 21426-21555  _resolve_youtube_ingest
  2279-2299   _resolver_stumm
 12466-12477  _restream_active_sources
 13403-13527  _restream_avatar_feeder_start
 13530-13539  _restream_avatar_feeder_stop
 17579-17697  _restream_chat_guardian
 12640-12712  _restream_chat_push
 12737-12746  _restream_chat_push_async
 13155-13264  _restream_html_overlay_start
 13267-13280  _restream_html_overlay_stop
 12425-12448  _restream_overlay_files
 18182-18214  _restream_platform_state
 18382-18417  _restream_resume_after_restart
 13587-13645  _restream_tts_enqueue_wav
 13016-13048  _restream_tts_feeder
 13013-13014  _restream_tts_fifo_path
 13542-13569  _restream_tts_start
 13571-13585  _restream_tts_stop
 18220-18379  _restream_verify_loop
 20493-20505  _retention_loop
 20487-20490  _retention_scan
  2623-2625   _room_is_abo
  5832-5949   _run_ai_call
 11802-11815  _run_async_from_flask
 19793-19796  _run_priv
 24764-24772  _run_selfcheck_and_exit
 20508-20519  _s3_client
  7796-7847   _safe_send
  4771-4787   _sample_net_throughput
  2577-2598   _schedule_next_check
 20441-20484  _scheduler_loop
  3997-4001   _schema_pk
 11819-11824  _scraper_session
 22124-22163  _screen_full
 11180-11217  _sec_headers
  2258-2260   _select_stream_from_data_section
 24514-24761  _selfcheck
  8583-8617   _send_live_notice
  1368-1372   _should_defer_upload
 20979-21014  _shrink_for_discord
  9750-9762   _sicheres_ziel
 20321-20359  _sicherheits_erinnerung_loop
 23692-23709  _sign_health_check
 23712-23731  _sign_health_loop
  4521-4546   _sitzung_bestimmen
  7607-7618   _spawn
 25189-25219  _spawn_from_flask
 17238-17517  _start_chat_listener
 11782-11799  _start_loop_watchdog
 11015-11061  _stats_loop
 10994-10997  _stats_output_path
 11000-11012  _stats_write
 19311-19325  _stimme_saubern
 19332-19356  _stimme_schon_gesagt
  8311-8327   _storage_cleanup_loop
 23751-23758  _story_for
  3418-3424   _stream_url_expiry
  3426-3431   _stream_url_ttl
 15460-15467  _streamer_persona_get
 20625-20747  _system_backup
 20756-20786  _system_backup_loop
 11624-11642  _task_auf_bot_schleife
 22937-22953  _telegram_befehlsmenue
  7661-7707   _telegram_polling_fehler
 10150-10189  _test_proxy
 10696-10712  _testpush_resolve_live
  7772-7793   _tg_sprache_setzen
  8490-8500   _tg_topics_load_into_mem
  8487-8488   _tg_topics_path
  8502-8509   _tg_topics_save
  9500-9508   _token_ok
  8512-8516   _topic_forget
 12095-12106  _tracking_max_duration
  4301-4315   _tracking_remove_cleanup
  4332-4344   _tracking_resume_cleanup
  1610-1633   _try_attach_file_handler
 19301-19309  _tts_cleanup
 10672-10676  _tunnel_effective
 23504-23524  _tunnel_lage
 23580-23632  _tunnel_wacht_loop
 18797-18850  _twitch_channel_status
 22166-22311  _twitch_chat_loop
 21270-21283  _twitch_clip_versuchen
 21980-22083  _twitch_eventsub_loop
  1391-1404   _upload_queue_add
  1415-1417   _upload_queue_count
  1374-1383   _upload_queue_load
  1364-1366   _upload_queue_path
  1406-1413   _upload_queue_remove
  1385-1389   _upload_queue_save
  1419-1460   _upload_window_loop
  7471-7478   _uptime_s
 12402-12411  _url_host
  3127-3221   _url_nachschlag
   860-864    _usage_record_claude
 23865-23887  _v37_pause_source
 23829-23839  _v37_restream_restart
 23842-23862  _v37_unpause_source
  7710-7754   _verbindung_verloren
  6561-6592   _viewer_sample_loop
  9589-9592   _wants_html
  7481-7495   _warn_empty_env
 23317-23438  _watchdog_loop
 21701-21709  _wchat_thank_ok
 17006-17036  _whisper_get_model
  7568-7575   _whisper_native_section
 16198-16204  _whisper_pool
 17130-17162  _whisper_segments
 17038-17054  _whisper_stumm
 17057-17127  _whisper_transcribe
 12808-12970  _write_restream_overlay
 12770-12805  _write_restream_overlay_async
 22335-22431  _youtube_api_chat_loop
 18853-18956  _youtube_api_status
 18959-19026  _youtube_channel_status
 22434-22595  _youtube_chat_loop
 21286-21311  _youtube_clip_versuchen
 21561-21574  _youtube_restream_autoconfig
 21577-21601  _youtube_restream_autoconfig_inner
 21668-21696  _youtube_send
 19094-19135  _youtube_set_channel
 21604-21638  _yt_access_token
 21641-21656  _yt_live_chat_id
 21664-21665  _yt_sendrate_cfg
 22314-22329  _yt_timeout
  2910-2911   _ytdlp_detect_available
  2913-2924   _ytdlp_note_result
 11669-11671  _zombie_child_count
  7347-7371   about
  4212-4216   add_ai_log_entry
  4129-4132   add_archive_entry
  4809-4811   add_archive_rule
  4549-4620   add_recording
  4276-4293   add_tracking
  5952-5985   ai
  3802-3875   ai_chat
  3909-3919   ai_history_append
  3921-3926   ai_history_clear
  3898-3907   ai_history_load
  3883-3896   ai_rate_limit_check
  6014-6022   aireset
 16537-16556  azrael_chat
 22600-22722  brain_cmd
  3434-3439   build_recording_cmd
  4296-4299   bulk_add_trackings
  6815-6874   bulkadd
  8330-8470   check_all_trackings
  4348-4360   claim_live_transition
 15537-16130  class KickModerator
 13706-15300  class RestreamManager
 10555-10597  classify_proxy_anonymity
  6060-6258   cleanup
  5099-5105   cleanup_old_recordings
  4494-4501   clear_recording
 21314-21383  clip_moment
  4761-4764   compute_storage_forecast
  6937-7010   cookies_cmd
  4267-4273   count_trackings_for_chat
  4199-4210   decide_preferred_recorder
  4139-4142   delete_archive_entry
  4813-4815   delete_archive_rule
  5489-5636   diag
 22834-22895  einnahmen_cmd
  4755-4758   find_recordings_by_fingerprint
  4160-4176   finish_recording_attempt
  4320-4322   get_all_active_trackings
  4227-4229   get_all_checks
  4622-4625   get_all_recordings
  4704-4706   get_all_tags_with_counts
  4732-4735   get_annotations_for_recording
  4134-4137   get_archive_entry
  4725-4728   get_bookmarked_recordings
  2118-2123   get_cookie_health
  4692-4698   get_event_log
  4183-4197   get_last_recording_attempt
  3224-3355   get_live_status
  5038-5041   get_manual_recordings
  4740-4743   get_or_compute_inspect_sync
  5140-5143   get_outcome_breakdown
  4711-4714   get_priority_poll_interval
  4178-4181   get_recent_recording_attempts
  4627-4630   get_recording_by_id
  4718-4721   get_recording_note
  3603-3626   get_redis
  4256-4259   get_stats
  5093-5097   get_storage_stats
  4833-4835   get_tiktok_status_distribution
  4362-4371   get_tracking_state
  4317-4318   get_trackings_for_group
  5054-5057   get_trash_recordings
  8875-9335   handle_recording_finished
 22929-22934  hilfe_cmd
  4024-4084   init_db
  4805-4807   list_archive_rules
  5293-5331   live
  7850-7858   live_check_worker
  3681-3715   llm_chat
  3738-3766   llm_chat_sync
  3723-3735   llm_list_models
  4651-4684   log_event
  1732-1765   log_recording_failure
  7160-7209   logs_cmd
 24227-24504  main
  5988-6011   on_ai_media
  7286-7312   on_ai_reply
  7315-7344   on_azrael_mention
  7376-7406   on_callback
 16562-16666  oracle_handle
  7049-7052   pause_tracking
  5153-5158   profile_keyboard
  7111-7157   quota
  8234-8308   reaper_loop
  4829-4831   record_tiktok_status
  6027-6057   recstatus
  3628-3636   redis_get_json
  3639-3645   redis_set_json
 22956-22966  report_cmd
 10600-10602  report_proxy_result
  2396-2438   resolve_tiktok_live_stream
  5049-5052   restore_recording
  7055-7058   resume_tracking
  4818-4823   run_archive_rules
 22969-23224  run_bot
 11521-11615  run_flask
  4793-4796   sample_bandwidth_for_active
  4219-4225   save_tiktok_check
  4486-4492   set_recording_file
  4325-4329   set_tracking_paused
  5044-5047   soft_delete_recording
  8623-8633   split_and_send_video
  5206-5248   start
  4144-4158   start_recording_attempt
  6261-6299   stats
  4983-5036   stop_manual_recording
  7061-7108   stoprec
  6485-6493   summary_cmd
  7212-7283   sysres
  5638-5782   teststream
  5250-5291   tiktok
  6877-6934   topusers
  5368-5425   track
  5333-5365   track_exact
  5439-5487   tracklist
  4867-4981   trigger_manual_recording
  4447-4484   try_acquire_recording_lock
  5060-5062   universal_search
 22898-22926  unpause_cmd
  5427-5437   untrack
 22725-22831  update_cmd
  4750-4753   update_recording_fingerprint
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
befehle.py             beschreibung, discord_nativ, discord_ueber_tg, fuer, hilfe_text, pruefen, telegram_handler
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
cookiebezug.py         anstossen, configure, faellig, gast_hilft, holen, info, intervall_s, naechster_lauf
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
lastvorsorge.py        freie_kerne, jung, startstufe
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
