# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
  9723  GET              /                                                dashboard
 11770  GET              /api/abo/status                                  api_abo_status
 11724  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 10511  GET              /api/automation/status                           api_automation_status
 10533  POST             /api/automation/toggle                           api_automation_toggle
 18955  GET              /api/channel/categories                          api_channel_categories
 18961  POST             /api/channel/set                                 api_channel_set
 18808  GET              /api/channels/status                             api_channels_status
 18482  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 18465  GET              /api/clips                                       api_clips
 18511  POST/DELETE      /api/clips/clear                                 api_clips_clear
 18390  GET              /api/debug/threads                               api_debug_threads
 11735  GET              /api/events                                      api_events
 11219  GET              /api/events/stream                               api_events_stream
 11046  GET              /api/health                                      api_health
 18424  POST             /api/highlights/config                           api_highlights_config
  9657  POST             /api/login                                       dashboard_login_submit
 12060  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11134  GET              /api/notify/status                               api_notify_status
 11145  POST             /api/notify/test                                 api_notify_test
 11824  GET              /api/proxy/heatmap                               api_proxy_heatmap
 11801  GET              /api/proxy/trend                                 api_proxy_trend
 18531  GET              /api/tts/<fn>                                    api_tts_file
 19306  GET              /api/upload_window                               api_upload_window
 11336  GET              /archive/<int:eid>/download                      archive_download
 11364  GET              /download/<int:recording_id>                     download
 11293  GET              /health                                          health
 18341  GET              /healthz                                         healthz
  9648  GET              /login                                           dashboard_login_page
  9678  GET              /logout                                          dashboard_logout
  9685  GET              /manifest.webmanifest                            pwa_manifest
 19279  GET              /overlay                                         overlay_page
  9709  GET              /pwa-icon-<variant>.png                          pwa_icon
  9695  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (335)

```
   182  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   404  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
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
   381  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   358  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
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
   425  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   434  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   419  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   239  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   195  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    73  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    80  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   479  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
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
   376  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   284  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   396  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   391  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   467  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
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
   410  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
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
   267  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   334  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   362  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   213  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   280  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   515  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    80  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   178  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   161  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   401  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
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
   329  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
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
   348  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
    92  GET              /api/selftest                                    api_selftest   [nc/routes/selbsttest.py]
   438  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
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
   371  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
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
   463  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   429  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   488  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   468  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   451  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   444  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
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

## Top-Level-Symbole in bot.py (506 Funktionen, 2 Klassen)

```
 23605-23627  _abbruch_datenbank_unlesbar
  2603-2604   _abo_key
  2624-2642   _abo_probe_dump
 23678-23696  _abschluss
 15291-15298  _ad_allowlist
 16267-16273  _agent_for
 16276-16292  _ai_telemetry
 16787-16805  _alert
 20165-20215  _alert_monitor_loop
 20567-20629  _announce_loop
  3365-3375   _anthropic_key
  3382-3384   _anthropic_model
  9343-9346   _arg_int
  2595-2600   _as_dict
 23355-23364  _async_exc_handler
 16968-16990  _audio_tap_cmd
 17527-17586  _audio_tap_melden
 17004-17028  _audio_tap_sammler
 23630-23665  _aufraeumen
  9511-9580   _auth_cookie
  9478-9507   _auth_guard
  1832-1837   _auto_on
 18203-18221  _auto_restream_loop
 13240-13282  _avatar_frames_laden
 21647-21662  _azrael_broadcast_reply
 21547-21569  _azrael_chat_reply
 21519-21544  _azrael_chat_should_reply
 21575-21577  _azrael_gate_cfg
 16297-16311  _azrael_live_state
 19192-19206  _azrael_overlay_state
 16669-16723  _azrael_proactive_loop
 16115-16171  _azrael_reaction_to_chats
 21580-21587  _azrael_reply_all_chats
 21506-21516  _azrael_self_names
 21615-21644  _azrael_send_to
 13201-13237  _azrael_spricht
 16317-16338  _azrael_system
 20299-20302  _backup_active
 20380-20393  _backup_loop
 23428-23437  _brain_crowdsec_snap
 20086-20095  _brain_growth_loop
  9902-9929   _brain_growth_snapshot
  2537-2557   _brain_hint_delay
 23500-23535  _brain_moderation_snap
  6244-6272   _brain_notify
 23538-23560  _brain_recording_snap
 23440-23497  _brain_restream_health
 23563-23576  _brain_tiktok_status_snap
 11198-11215  _browser_push
  6284-6371   _build_daily_summary
 13561-13565  _build_restream_cmd
  5066-5093   _can_stop_tracking
  1945-1967   _capture_set_cookies
 11878-11881  _cfg_get
 11884-11886  _cfg_set
 18916-18951  _channel_set_all
 12429-12432  _chat_connected
 12435-12451  _chat_disconnected
  8410-8421   _chat_is_forum
 17334-17359  _chat_listener_abbauen
 12471-12473  _chat_sanitize
 12414-12426  _chat_stat
 12454-12457  _chat_stats_snapshot
  3668-3680   _check_ai_models_sync
 10184-10227  _classify_pool_anonymity
 10230-10247  _classify_pool_anonymity_bg
   860-882    _claude_chat_sync_metered
  9372-9379   _client_ip
 20713-20740  _clip_prune
 20743-20753  _clip_recfile_for
 21163-21169  _clip_should_velocity
 20794-20876  _clip_to_discord
  3561-3570   _close_ai_session
 21693-21708  _cohost_broadcast
 21678-21679  _cohost_cfg
 21734-21746  _cohost_fire_highlight
 21682-21690  _cohost_gate
 21711-21731  _cohost_highlight
  9832-9834   _conv_messages
  6643-6704   _cookie_alarm_loop
  2036-2041   _cookie_autofetch_info
  2019-2023   _cookie_autorefresh_info
  1922-1926   _cookie_header
  2053-2086   _cookies_selbst_holen
  3896-3908   _create_index_safe
 19638-19744  _crowdsec_status
 19584-19635  _crowdsec_via_lapi
 19488-19506  _cscli_bin
 19515-19528  _cscli_path
  6533-6558   _daily_summary_loop
 19546-19563  _darf_journal_lesen
  3017-3042   _darf_ytdlp_nachschlagen
 11379-11400  _dashboard_adresse
 20139-20162  _db_maintenance_loop
  6502-6530   _db_vacuum_loop
 15314-15338  _detect_foreign_ad
  1545-1556   _diag_path_owner
 16575-16619  _director_finalize
 17516-17523  _director_for
 16524-16572  _director_mark
 21028-21031  _disc_state_get
 21034-21041  _disc_state_set
 20067-20076  _discord_bot_starten
 20031-20042  _discord_einladung_merken
 20079-20083  _discord_invite
 20045-20064  _discord_kontext
 20989-21025  _discord_live_thread
 16726-16738  _discord_notify
 20003-20028  _discord_ops_alert
 20887-20985  _discord_post_user
 20632-20638  _discord_stop
  6561-6638   _disk_alarm_loop
 23158-23207  _disk_autoclean
 23210-23223  _disk_guard_loop
 13179-13186  _drossel_hoeher
 13175-13176  _drossel_stufe
 13189-13197  _drossel_zuruecksetzen
 11556-11558  _dump_all_threads
 10110-10173  _enrich_proxies_with_geo
  2115-2176   _ensure_cookie_file_netscape
  8469-8472   _ensure_notify_topic
 10354-10391  _ensure_proxy_ready
  8423-8450   _ensure_topic
   709-711    _env_int
   714-716    _env_int_range
 16771-16784  _event_webhook
 12229-12242  _evolution_loop
  5686-5720   _extract_file_payload
  2248-2250   _extract_urls_from_streamurl_node
 19531-19538  _f2b_sudo_hint
 23699-23762  _fatal_vom_botteil
  4530-4540   _fehler_text
 10011-10029  _fetch_proxy_list
 17303-17331  _fetch_tiktok_room_id
   792-795    _ff_cmd
 13008-13013  _find_chromium
  3285-3287   _find_external_recorder
  2253-2255   _find_stream_urls
 11929-11954  _fire_webhooks
  7470-7479   _fork_safe
   893-906    _freeai_chat_sync_metered
 19577-19581  _geo_lookup_ips
  3549-3558   _get_ai_session
  7303-7343   _get_live_info
  2869-2876   _get_resolve_semaphore
  7752-8124   _handle_single_tracking
 22980-22982  _hb
 22985-23002  _hb_while
 12485-12487  _highlight_cfg
 12490-12519  _highlight_observe
 13016-13034  _htmlov_screenshot_cmd
 17030-17040  _httpx_proxy
 11962-11974  _in_quiet_hours
 23591-23602  _init_db_oder_abbruch
 24314-24345  _install_fast_eventloop
  9238-9292   _install_fast_json
 11561-11577  _install_faulthandler
 18249-18258  _intel_ensure_schema
 18296-18331  _intel_index_loop
 18270-18280  _intel_index_one
 18261-18267  _intel_semantic
  5055-5064   _is_authorized
  7653-7659   _is_dead
  2238-2240   _is_hevc
 19566-19568  _is_private_ip
  1731-1738   _is_process_running
  6274-6281   _is_quiet_hours
  1338-1347   _is_upload_window
  4395-4410   _iso
  9327-9340   _json_error_handler
  6496-6497   _kick_broadcaster_id
  6408-6450   _kick_follower_count
  6392-6395   _kick_slug
 11011-11018  _kick_user_token
 23579-23588  _kickmod_boot
  3985-3988   _kind_from_filename
 11991-11993  _latest_popularity
 17912-17961  _live_react_loop
 17589-17901  _live_react_worker
 16174-16185  _live_transcript_push
 17903-17910  _live_users
 16622-16666  _living_title_loop
 20305-20377  _local_backup_scan
  9309-9323   _log_5xx
   782-789    _log_sicher
 13573-13585  _looks_like_codec_err
 13568-13570  _looks_like_source_expired
  7520-7550   _loop_fehler
 11581-11590  _loop_heartbeat
 22950-22977  _loop_lag_monitor
 11593-11661  _loop_watchdog_thread
 16054-16068  _loyalty_add
 16045-16051  _loyalty_get
 16071-16079  _loyalty_top
 12101-12103  _manual_donations_total
  4737-4756   _manual_status
  7661-7662   _mark_dead
 10630-10646  _marketing_loop
 21594-21612  _maybe_handle_command
 23309-23333  _maybe_hype_clip
 20682-20710  _meme_klassifizieren
  3863-3886   _migrate_columns
 21873-21884  _mod_is_exempt
 21887-21892  _mod_warn_first
 21895-21898  _mod_warn_text
 12269-12277  _modlog
  1038-1040   _multistream_targets
  3045-3081   _nachschlag_ytdlp
  7482-7483   _nc_create_subprocess_exec
  7486-7487   _nc_create_subprocess_shell
 10948-10965  _news_loop
 12296-12298  _normalize_ingest
  2468-2485   _note_check_duration
  8463-8466   _notify_topic_name
 16200-16208  _oracle_memories
 16473-16507  _oracle_memorize
 16211-16224  _oracle_persona
 16193-16197  _oracle_recent_text
 12642-12643  _ov_atomic_write
 12633-12635  _ov_bar
 15217-15229  _ov_clip_text
 12638-12639  _ov_oneline
 19243-19272  _overlay_push
 12962-13005  _overlay_render_size
 12365-12369  _overlay_session_reset
 19208-19210  _overlay_src_ok
 15301-15311  _own_invites
 12957-12959  _parse_size
 19752-19832  _parse_ssh_attacks
  6905-6938   _pause_resume_cmd
  1973-2017   _persist_refreshed_cookies
  1876-1908   _pick_checked_pull_proxy
  9408-9421   _pin_auth_value
  9467-9468   _pin_clear_fail
  9447-9450   _pin_locked
  9453-9464   _pin_note_fail
  9424-9444   _pin_ok
 19052-19077  _piper_pick_model
 19137-19186  _piper_say
 11891-11926  _post_json_threaded
 12936-12954  _probe_video_size
  1759-1776   _proc_is_recorder
 10323-10351  _proxy_pool_refresh_loop
  1842-1873   _proxy_report_recording
 11546-11548  _prune_stall_dumps
 10700-10870  _public_stats
  2044-2050   _pull_proxy_still
 16742-16768  _push_notify
  9627-9629   _pwa_dir
 10080-10095  _quick_validate_proxy
 11957-11959  _quiet_hours_config
  9592-9625   _rate_guard
 16015-16021  _react_warn
  7390-7429   _reap_proc
  8693-8760   _rec_auto_abschalten
  8640-8690   _rec_frueh_getrennt
  8527-8585   _rec_kategorie_melden
  8588-8637   _rec_totstreak_fortschreiben
  2508-2530   _record_check_outcome
   777-779    _redact_stream_urls
 10250-10320  _refresh_proxy_pool
  2285-2376   _resolve_via_html
  2649-2846   _resolve_via_webcast_api_v2
  2909-2996   _resolve_via_ytdlp
 21203-21332  _resolve_youtube_ingest
  2264-2282   _resolver_stumm
 12348-12359  _restream_active_sources
 13285-13409  _restream_avatar_feeder_start
 13412-13421  _restream_avatar_feeder_stop
 17362-17480  _restream_chat_guardian
 12522-12594  _restream_chat_push
 12619-12628  _restream_chat_push_async
 13037-13146  _restream_html_overlay_start
 13149-13162  _restream_html_overlay_stop
 12307-12330  _restream_overlay_files
 17965-17997  _restream_platform_state
 18165-18200  _restream_resume_after_restart
 13469-13527  _restream_tts_enqueue_wav
 12898-12930  _restream_tts_feeder
 12895-12896  _restream_tts_fifo_path
 13424-13451  _restream_tts_start
 13453-13467  _restream_tts_stop
 18003-18162  _restream_verify_loop
 20270-20282  _retention_loop
 20264-20267  _retention_scan
  2606-2608   _room_is_abo
  5724-5841   _run_ai_call
 11684-11697  _run_async_from_flask
 19571-19574  _run_priv
 24302-24310  _run_selfcheck_and_exit
 20285-20296  _s3_client
  7688-7739   _safe_send
  4663-4679   _sample_net_throughput
  2560-2581   _schedule_next_check
 20218-20261  _scheduler_loop
  3889-3893   _schema_pk
 11701-11706  _scraper_session
 21901-21940  _screen_full
 11062-11099  _sec_headers
  2243-2245   _select_stream_from_data_section
 24052-24299  _selfcheck
  8475-8509   _send_live_notice
  1361-1365   _should_defer_upload
 20756-20791  _shrink_for_discord
  9632-9644   _sicheres_ziel
 20098-20136  _sicherheits_erinnerung_loop
 23230-23247  _sign_health_check
 23250-23269  _sign_health_loop
  4413-4438   _sitzung_bestimmen
  7499-7510   _spawn
 24720-24750  _spawn_from_flask
 17042-17300  _start_chat_listener
 11664-11681  _start_loop_watchdog
 10897-10943  _stats_loop
 10876-10879  _stats_output_path
 10882-10894  _stats_write
 19089-19103  _stimme_saubern
 19110-19134  _stimme_schon_gesagt
  8203-8219   _storage_cleanup_loop
 23289-23296  _story_for
  3310-3316   _stream_url_expiry
  3318-3323   _stream_url_ttl
 15264-15271  _streamer_persona_get
 20402-20524  _system_backup
 20533-20563  _system_backup_loop
 11506-11524  _task_auf_bot_schleife
  7553-7599   _telegram_polling_fehler
 10032-10071  _test_proxy
 10578-10594  _testpush_resolve_live
  7664-7685   _tg_sprache_setzen
  8382-8392   _tg_topics_load_into_mem
  8379-8380   _tg_topics_path
  8394-8401   _tg_topics_save
  9382-9390   _token_ok
  8404-8408   _topic_forget
 11977-11988  _tracking_max_duration
  4193-4207   _tracking_remove_cleanup
  4224-4236   _tracking_resume_cleanup
  1603-1626   _try_attach_file_handler
 19079-19087  _tts_cleanup
 10554-10558  _tunnel_effective
 18575-18628  _twitch_channel_status
 21943-22088  _twitch_chat_loop
 21047-21060  _twitch_clip_versuchen
 21757-21860  _twitch_eventsub_loop
  1384-1397   _upload_queue_add
  1408-1410   _upload_queue_count
  1367-1376   _upload_queue_load
  1357-1359   _upload_queue_path
  1399-1406   _upload_queue_remove
  1378-1382   _upload_queue_save
  1412-1453   _upload_window_loop
  7363-7370   _uptime_s
 12284-12293  _url_host
   853-857    _usage_record_claude
 23403-23425  _v37_pause_source
 23367-23377  _v37_restream_restart
 23380-23400  _v37_unpause_source
  7602-7646   _verbindung_verloren
  6453-6484   _viewer_sample_loop
  9471-9474   _wants_html
  7373-7387   _warn_empty_env
 23023-23144  _watchdog_loop
 21478-21486  _wchat_thank_ok
 16810-16840  _whisper_get_model
  7460-7467   _whisper_native_section
 16002-16008  _whisper_pool
 16934-16966  _whisper_segments
 16842-16858  _whisper_stumm
 16861-16931  _whisper_transcribe
 12690-12852  _write_restream_overlay
 12652-12687  _write_restream_overlay_async
 22112-22208  _youtube_api_chat_loop
 18631-18734  _youtube_api_status
 18737-18804  _youtube_channel_status
 22211-22372  _youtube_chat_loop
 21063-21088  _youtube_clip_versuchen
 21338-21351  _youtube_restream_autoconfig
 21354-21378  _youtube_restream_autoconfig_inner
 21445-21473  _youtube_send
 18872-18913  _youtube_set_channel
 21381-21415  _yt_access_token
 21418-21433  _yt_live_chat_id
 21441-21442  _yt_sendrate_cfg
 22091-22106  _yt_timeout
  2893-2894   _ytdlp_detect_available
  2896-2907   _ytdlp_note_result
 11551-11553  _zombie_child_count
  7239-7263   about
  4104-4108   add_ai_log_entry
  4021-4024   add_archive_entry
  4701-4703   add_archive_rule
  4441-4512   add_recording
  4168-4185   add_tracking
  5844-5877   ai
  3694-3767   ai_chat
  3801-3811   ai_history_append
  3813-3818   ai_history_clear
  3790-3799   ai_history_load
  3775-3788   ai_rate_limit_check
  5906-5914   aireset
 16341-16360  azrael_chat
 22377-22499  brain_cmd
  3326-3331   build_recording_cmd
  4188-4191   bulk_add_trackings
  6707-6766   bulkadd
  8222-8362   check_all_trackings
  4240-4252   claim_live_transition
 15341-15934  class KickModerator
 13588-15104  class RestreamManager
 10437-10479  classify_proxy_anonymity
  5952-6150   cleanup
  4991-4997   cleanup_old_recordings
  4386-4393   clear_recording
 21091-21160  clip_moment
  4653-4656   compute_storage_forecast
  6829-6902   cookies_cmd
  4159-4165   count_trackings_for_chat
  4091-4102   decide_preferred_recorder
  4031-4034   delete_archive_entry
  4705-4707   delete_archive_rule
  5381-5528   diag
 22611-22672  einnahmen_cmd
  4647-4650   find_recordings_by_fingerprint
  4052-4068   finish_recording_attempt
  4212-4214   get_all_active_trackings
  4119-4121   get_all_checks
  4514-4517   get_all_recordings
  4596-4598   get_all_tags_with_counts
  4624-4627   get_annotations_for_recording
  4026-4029   get_archive_entry
  4617-4620   get_bookmarked_recordings
  2103-2108   get_cookie_health
  4584-4590   get_event_log
  4075-4089   get_last_recording_attempt
  3084-3247   get_live_status
  4930-4933   get_manual_recordings
  4632-4635   get_or_compute_inspect_sync
  5032-5035   get_outcome_breakdown
  4603-4606   get_priority_poll_interval
  4070-4073   get_recent_recording_attempts
  4519-4522   get_recording_by_id
  4610-4613   get_recording_note
  3495-3518   get_redis
  4148-4151   get_stats
  4985-4989   get_storage_stats
  4725-4727   get_tiktok_status_distribution
  4254-4263   get_tracking_state
  4209-4210   get_trackings_for_group
  4946-4949   get_trash_recordings
  8763-9217   handle_recording_finished
  3916-3976   init_db
  4697-4699   list_archive_rules
  5185-5223   live
  7742-7750   live_check_worker
  3573-3607   llm_chat
  3630-3658   llm_chat_sync
  3615-3627   llm_list_models
  4543-4576   log_event
  1693-1726   log_recording_failure
  7052-7101   logs_cmd
 23765-24042  main
  5880-5903   on_ai_media
  7178-7204   on_ai_reply
  7207-7236   on_azrael_mention
  7268-7298   on_callback
 16366-16470  oracle_handle
  6941-6944   pause_tracking
  5045-5050   profile_keyboard
  7003-7049   quota
  8126-8200   reaper_loop
  4721-4723   record_tiktok_status
  5919-5949   recstatus
  3520-3528   redis_get_json
  3531-3537   redis_set_json
 22675-22685  report_cmd
 10482-10484  report_proxy_result
  2379-2421   resolve_tiktok_live_stream
  4941-4944   restore_recording
  6947-6950   resume_tracking
  4710-4715   run_archive_rules
 22688-22930  run_bot
 11403-11497  run_flask
  4685-4688   sample_bandwidth_for_active
  4111-4117   save_tiktok_check
  4378-4384   set_recording_file
  4217-4221   set_tracking_paused
  4936-4939   soft_delete_recording
  8515-8525   split_and_send_video
  5098-5140   start
  4036-4050   start_recording_attempt
  6153-6191   stats
  4875-4928   stop_manual_recording
  6953-7000   stoprec
  6377-6385   summary_cmd
  7104-7175   sysres
  5530-5674   teststream
  5142-5183   tiktok
  6769-6826   topusers
  5260-5317   track
  5225-5257   track_exact
  5331-5379   tracklist
  4759-4873   trigger_manual_recording
  4339-4376   try_acquire_recording_lock
  4952-4954   universal_search
  5319-5329   untrack
 22502-22608  update_cmd
  4642-4645   update_recording_fingerprint
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
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
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
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
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
