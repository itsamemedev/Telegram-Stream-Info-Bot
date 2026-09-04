# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (42)

```
 10070  GET              /                                                dashboard
 12252  GET              /api/abo/status                                  api_abo_status
 12206  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 10858  GET              /api/automation/status                           api_automation_status
 10880  POST             /api/automation/toggle                           api_automation_toggle
 19021  GET              /api/channel/categories                          api_channel_categories
 19027  POST             /api/channel/set                                 api_channel_set
 18874  GET              /api/channels/status                             api_channels_status
 18548  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 18531  GET              /api/clips                                       api_clips
 18577  POST/DELETE      /api/clips/clear                                 api_clips_clear
 18456  GET              /api/debug/threads                               api_debug_threads
 12217  GET              /api/events                                      api_events
 11684  GET              /api/events/stream                               api_events_stream
 11350  GET              /api/health                                      api_health
 18490  POST             /api/highlights/config                           api_highlights_config
 10004  POST             /api/login                                       dashboard_login_submit
 12545  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11599  GET              /api/notify/status                               api_notify_status
 11610  POST             /api/notify/test                                 api_notify_test
 12306  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12283  GET              /api/proxy/trend                                 api_proxy_trend
 19949  GET              /api/selftest                                    api_selftest
 11909  GET              /api/system                                      api_system
 12600  GET              /api/system/check_timing                         api_check_timing
 12692  GET              /api/system/config_drift                         api_config_drift
 11415  GET              /api/system/config_snapshot                      api_system_config_snapshot
 11457  GET              /api/system/preflight                            api_system_preflight
 11583  GET              /api/system/preflight_history                    api_system_preflight_history
 11749  GET              /api/system/resilience                           api_system_resilience
 18597  GET              /api/tts/<fn>                                    api_tts_file
 19323  GET              /api/upload_window                               api_upload_window
 11882  GET              /archive/<int:eid>/download                      archive_download
 11939  GET              /download/<int:recording_id>                     download
 11839  GET              /health                                          health
 18425  GET              /healthz                                         healthz
  9995  GET              /login                                           dashboard_login_page
 10025  GET              /logout                                          dashboard_logout
 10032  GET              /manifest.webmanifest                            pwa_manifest
 19296  GET              /overlay                                         overlay_page
 10056  GET              /pwa-icon-<variant>.png                          pwa_icon
 10042  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (317)

```
   173  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   380  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   185  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   155  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   994  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   734  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   865  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   845  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   883  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   807  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   347  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   358  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   368  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   391  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   398  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   409  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   542  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   640  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1232  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1264  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   331  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   947  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   927  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1100  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1148  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1199  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1058  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   902  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   366  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   630  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   512  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   495  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   487  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   323  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   339  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   674  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   639  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   659  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   546  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    40  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    69  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   216  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   241  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   246  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
   154  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    90  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   213  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   111  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   333  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   319  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   341  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   165  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   397  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   388  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   305  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   181  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   222  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   234  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   363  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   272  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   258  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   370  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
   277  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   208  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   174  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   157  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   357  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   334  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
   184  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   121  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   106  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    83  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   144  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    70  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    72  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    44  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
   152  GET              /api/checks                                      api_checks   [nc/routes/auskunft.py]
    31  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    43  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    42  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    77  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   112  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   401  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   274  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   259  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   182  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
    60  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    67  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   455  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   203  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   230  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   190  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
   155  GET              /api/defense/attacks                             api_defense_attacks   [nc/routes/abwehr.py]
   116  GET              /api/defense/crowdsec                            api_defense_crowdsec   [nc/routes/abwehr.py]
   137  GET              /api/defense/fail2ban                            api_defense_fail2ban   [nc/routes/abwehr.py]
    82  GET              /api/defense/overview                            api_defense_overview   [nc/routes/abwehr.py]
   235  POST             /api/discord/announce                            api_discord_announce   [nc/routes/discord.py]
   161  GET              /api/discord/clips_week                          api_discord_clips_week   [nc/routes/discord.py]
   179  GET              /api/discord/community                           api_discord_community   [nc/routes/discord.py]
   151  GET              /api/discord/invite                              api_discord_invite   [nc/routes/discord.py]
    54  GET              /api/discord/overview                            api_discord_overview   [nc/routes/discord.py]
   127  POST             /api/discord/webhook_test                        api_discord_webhook_test   [nc/routes/discord.py]
    70  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
   103  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   111  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    51  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   127  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
   156  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   141  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    81  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   103  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   124  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
    71  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   171  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    35  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   191  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   211  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   238  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
   352  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   275  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   372  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   367  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   443  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
    64  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    53  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   220  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    77  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   158  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    33  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   140  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   115  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   179  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    66  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    89  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   213  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   210  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   232  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
    91  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   159  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   137  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    76  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   116  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   166  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   110  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   158  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   175  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   206  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   182  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   242  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   212  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    73  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   226  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
   386  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
    69  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
    94  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   104  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    43  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    61  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   215  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
    91  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    57  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    68  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   133  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   128  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   119  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    44  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    83  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   258  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   325  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   353  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   204  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   271  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   506  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    71  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   169  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   152  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   392  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   216  GET              /api/outcomes                                    api_outcomes   [nc/routes/auskunft.py]
   210  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   193  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
    94  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   168  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   451  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   426  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   287  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   133  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   823  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   905  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   933  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   944  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   810  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   872  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   859  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   840  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   305  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   485  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   480  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   528  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   411  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   738  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   502  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   465  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   438  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   712  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   582  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   671  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   577  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   510  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   290  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   755  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   378  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   633  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   788  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   773  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   334  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   572  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   558  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   541  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   598  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
   691  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   587  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   477  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   455  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   496  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   513  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   565  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   431  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   256  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   156  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   587  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   404  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   125  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   526  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   552  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   182  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   207  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   379  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   134  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   144  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   315  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   305  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   340  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    56  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    77  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    43  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
    93  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   324  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
   414  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
   118  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   209  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   204  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   264  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   110  GET              /api/storage                                     api_storage   [nc/routes/wartung.py]
   116  POST             /api/storage/cleanup                             api_storage_cleanup   [nc/routes/wartung.py]
   439  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   331  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   361  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
   117  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   264  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    79  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   289  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   221  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   245  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   176  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   141  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   201  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    47  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   197  GET              /api/summary/preview                             api_summary_preview   [nc/routes/auskunft.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   347  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
   167  GET              /api/top                                         api_top   [nc/routes/auskunft.py]
   228  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   443  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   472  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   392  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   405  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   501  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   378  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   253  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   298  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   322  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   309  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   155  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   267  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   125  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   359  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   414  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   243  GET              /api/trend-7d                                    api_trend_7d   [nc/routes/auskunft.py]
   112  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
    91  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   123  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   104  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   115  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    67  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
    91  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    45  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   454  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   420  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   479  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   459  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   442  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   435  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
   229  GET              /api/userstats                                   api_userstats   [nc/routes/auskunft.py]
   296  GET              /api/version                                     api_version   [nc/routes/auskunft.py]
    42  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    82  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   113  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
    97  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   122  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   143  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   155  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    80  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
   104  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    58  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   190  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
   373  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands (45)

```
 20633  /ai                     
 21106  /ask                    
 20724  /assign_role            
 20770  /ban                    
 21438  /botstats               
 21362  /clearwarns             
 21402  /clip                   
 21387  /clipoftheweek          
 21229  /clips                  
 20685  /create_category        
 20654  /create_channel         
 20713  /create_group           
 20696  /create_role            
 20670  /create_voice           
 21006  /daily                  
 21136  /event                  
 21179  /events                 
 21275  /follow                 
 21259  /help                   
 20759  /kick                   
 20988  /leaderboard            
 21215  /livenow                
 21245  /post_test              
 21076  /profile                
 20794  /purge                  
 20974  /rank                   
 21202  /recstatus              
 20735  /remove_role            
 20647  /restream_status        
 20746  /set_channel_perms      
 20939  /setup_community        
 20957  /setup_targets          
 21301  /stats                  
 20559  /status                 
 21597  /streaminfo             
 21494  /sys_report             
 21470  /sys_unpause            
 20781  /timeout                
 21373  /topstreamers           
 20589  /track                  
 20573  /tracklist              
 21290  /unfollow               
 20622  /untrack                
 21323  /warn                   
 21347  /warnings               
```

## Discord-Events (4)

```
 22083  on_member_join
 22045  on_message
 21684  on_raw_reaction_add
 22118  on_ready
```

## Top-Level-Symbole in bot.py (479 Funktionen, 2 Klassen)

```
  2548-2549   _abo_key
  2569-2587   _abo_probe_dump
 19533-19543  _active_recorder_sync
 15585-15592  _ad_allowlist
 16726-16732  _agent_for
 19545-19563  _ai_calls_total_sync
 16735-16751  _ai_telemetry
 17240-17258  _alert
 22234-22284  _alert_monitor_loop
 22636-22698  _announce_loop
  3490-3493   _anthropic_key
  3500-3502   _anthropic_model
  9748-9751   _arg_int
  2540-2545   _as_dict
 17394-17416  _audio_tap_cmd
  9916-9927   _auth_cookie
  9883-9912   _auth_guard
  1711-1716   _auto_on
 18287-18305  _auto_restream_loop
 23777-23792  _azrael_broadcast_reply
 23677-23699  _azrael_chat_reply
 23660-23674  _azrael_chat_should_reply
 23705-23707  _azrael_gate_cfg
 16756-16770  _azrael_live_state
 19208-19222  _azrael_overlay_state
 17122-17176  _azrael_proactive_loop
 16574-16630  _azrael_reaction_to_chats
 23710-23717  _azrael_reply_all_chats
 23647-23657  _azrael_self_names
 23745-23774  _azrael_send_to
 16776-16797  _azrael_system
 22368-22371  _backup_active
 22449-22462  _backup_loop
 22196-22205  _brain_growth_loop
 10249-10276  _brain_growth_snapshot
  2476-2496   _brain_hint_delay
  6160-6188   _brain_notify
 11663-11680  _browser_push
  6204-6291   _build_daily_summary
  2979-3159   _build_native_cmd
 13771-13958  _build_restream_cmd
  3203-3236   _build_ytdlp_cmd
 19485-19492  _cached_probe
  4982-5009   _can_stop_tracking
  1891-1913   _capture_set_cookies
 12360-12363  _cfg_get
 12366-12368  _cfg_set
 18982-19017  _channel_set_all
 12964-12967  _chat_connected
 12970-12986  _chat_disconnected
  8239-8250   _chat_is_forum
 13006-13008  _chat_sanitize
 12949-12961  _chat_stat
 12989-12992  _chat_stats_snapshot
  3768-3779   _check_ai_alive_sync
  3782-3794   _check_ai_models_sync
 19494-19507  _check_redis_alive_sync
 19509-19529  _check_redis_version_sync
 10531-10574  _classify_pool_anonymity
 10577-10594  _classify_pool_anonymity_bg
   827-849    _claude_chat_sync_metered
  9777-9784   _client_ip
 22730-22757  _clip_prune
 22760-22770  _clip_recfile_for
 23311-23317  _clip_should_velocity
 22811-22893  _clip_to_discord
  3666-3675   _close_ai_session
 23823-23838  _cohost_broadcast
 23808-23809  _cohost_cfg
 23864-23876  _cohost_fire_highlight
 23812-23820  _cohost_gate
 23841-23861  _cohost_highlight
 22942-23004  _community_events_loop
 10179-10181  _conv_messages
  6563-6606   _cookie_alarm_loop
  1963-1967   _cookie_autorefresh_info
  1868-1872   _cookie_header
 11713-11745  _cpu_load_snapshot
  3988-4000   _create_index_safe
 19727-19833  _crowdsec_status
 19673-19724  _crowdsec_via_lapi
 19577-19595  _cscli_bin
 19604-19617  _cscli_path
  6453-6478   _daily_summary_loop
 19635-19652  _darf_journal_lesen
 22208-22231  _db_maintenance_loop
  6422-6450   _db_vacuum_loop
 15608-15632  _detect_foreign_ad
  1446-1457   _diag_path_owner
 17028-17072  _director_finalize
 17840-17847  _director_for
 16977-17025  _director_mark
 23205-23240  _disc_automod_check
 23181-23184  _disc_state_get
 23187-23194  _disc_state_set
 20209-20222  _discord_guild_filesize_bytes
 20416-20420  _discord_invite
 23142-23178  _discord_live_thread
 17179-17191  _discord_notify
 20315-20340  _discord_ops_alert
 23040-23138  _discord_post_user
 20476-22193  _discord_run_once
 20355-20413  _discord_start
 22701-22707  _discord_stop
 20230-20232  _discord_upload_limit_label
 20225-20227  _discord_upload_limit_mb
  6481-6558   _disk_alarm_loop
 25256-25305  _disk_autoclean
 25308-25321  _disk_guard_loop
 25248-25253  _disk_pct
 13364-13366  _drawtext_chain
 12038-12040  _dump_all_threads
 10457-10520  _enrich_proxies_with_geo
  2108-2152   _ensure_cookie_file_netscape
 20423-20473  _ensure_discord_invite
 22907-22939  _ensure_error_channel
  8298-8301   _ensure_notify_topic
 10701-10738  _ensure_proxy_ready
  8252-8279   _ensure_topic
   684-686    _env_int
   689-691    _env_int_range
 23007-23037  _error_channel_loop
 17224-17237  _event_webhook
 12779-12792  _evolution_loop
  5602-5636   _extract_file_payload
  2224-2226   _extract_urls_from_streamurl_node
 19620-19627  _f2b_sudo_hint
 17260-17262  _faster_whisper_available
 10358-10376  _fetch_proxy_list
 17674-17702  _fetch_tiktok_room_id
   760-763    _ff_cmd
 13530-13535  _find_chromium
  3196-3200   _find_external_recorder
  2229-2231   _find_stream_urls
 12411-12436  _fire_webhooks
  7343-7352   _fork_safe
   860-873    _freeai_chat_sync_metered
 19666-19670  _geo_lookup_ips
  3654-3663   _get_ai_session
  7176-7216   _get_live_info
  2766-2773   _get_resolve_semaphore
  7576-7953   _handle_single_tracking
 25074-25076  _hb
 25079-25096  _hb_while
 13020-13022  _highlight_cfg
 13025-13054  _highlight_observe
 13538-13556  _htmlov_screenshot_cmd
 17418-17428  _httpx_proxy
 12444-12456  _in_quiet_hours
 26147-26178  _install_fast_eventloop
  9643-9697   _install_fast_json
 12043-12059  _install_faulthandler
 18333-18342  _intel_ensure_schema
 18380-18415  _intel_index_loop
 18354-18364  _intel_index_one
 18345-18351  _intel_semantic
  4971-4980   _is_authorized
  7477-7483   _is_dead
  2214-2216   _is_hevc
 19655-19657  _is_private_ip
  1610-1617   _is_process_running
  6190-6201   _is_quiet_hours
  1247-1256   _is_upload_window
  9732-9745   _json_error_handler
  6416-6417   _kick_broadcaster_id
  6328-6370   _kick_follower_count
  6312-6315   _kick_slug
 11291-11322  _kick_user_token
  4037-4040   _kind_from_filename
 12473-12478  _latest_popularity
 18055-18088  _live_react_loop
 17851-18044  _live_react_worker
 16633-16644  _live_transcript_push
 18046-18053  _live_users
 17075-17119  _living_title_loop
  1789-1862   _load_cookies_dict
 22374-22446  _local_backup_scan
  9714-9728   _log_5xx
 13966-13978  _looks_like_codec_err
 13961-13963  _looks_like_source_expired
  7393-7423   _loop_fehler
 12063-12072  _loop_heartbeat
 25044-25071  _loop_lag_monitor
 12075-12143  _loop_watchdog_thread
 16513-16527  _loyalty_add
 16504-16510  _loyalty_get
 16530-16538  _loyalty_top
 12586-12588  _manual_donations_total
  7485-7486   _mark_dead
 10977-10993  _marketing_loop
 23724-23742  _maybe_handle_command
 25407-25431  _maybe_hype_clip
  3955-3978   _migrate_columns
 24003-24014  _mod_is_exempt
 24017-24022  _mod_warn_first
 24025-24028  _mod_warn_text
 12819-12827  _modlog
   998-1000   _multistream_targets
  7355-7356   _nc_create_subprocess_exec
  7359-7360   _nc_create_subprocess_shell
 11228-11245  _news_loop
 12846-12848  _normalize_ingest
  2407-2424   _note_check_duration
  8292-8295   _notify_topic_name
 16659-16667  _oracle_memories
 16932-16966  _oracle_memorize
 16670-16683  _oracle_persona
 16652-16656  _oracle_recent_text
 13145-13153  _ov_atomic_write
 13133-13139  _ov_bar
 15511-15523  _ov_clip_text
 13142-13143  _ov_oneline
 19260-19289  _overlay_push
 13484-13527  _overlay_render_size
 12912-12916  _overlay_session_reset
 19224-19227  _overlay_src_ok
 15595-15605  _own_invites
 13479-13481  _parse_size
 19841-19921  _parse_ssh_attacks
  6778-6811   _pause_resume_cmd
  1917-1961   _persist_refreshed_cookies
  1755-1787   _pick_checked_pull_proxy
  9813-9826   _pin_auth_value
  9872-9873   _pin_clear_fail
  9852-9855   _pin_locked
  9858-9869   _pin_note_fail
  9829-9849   _pin_ok
 19118-19143  _piper_pick_model
 19155-19202  _piper_say
 12373-12408  _post_json_threaded
 13458-13476  _probe_video_size
  1638-1655   _proc_is_recorder
 10670-10698  _proxy_pool_refresh_loop
  1721-1752   _proxy_report_recording
 12028-12030  _prune_stall_dumps
 11047-11168  _public_stats
 17195-17221  _push_notify
  9974-9976   _pwa_dir
 10427-10442  _quick_validate_proxy
 12439-12441  _quiet_hours_config
  9939-9972   _rate_guard
 16478-16484  _react_warn
  7263-7302   _reap_proc
  2447-2469   _record_check_outcome
   755-757    _redact_stream_urls
 10597-10667  _refresh_proxy_pool
  2240-2330   _resolve_via_html
  2589-2743   _resolve_via_webcast_api_v2
  2806-2868   _resolve_via_ytdlp
 23351-23480  _resolve_youtube_ingest
 12895-12906  _restream_active_sources
 17705-17804  _restream_chat_guardian
 13057-13129  _restream_chat_push
 13559-13646  _restream_html_overlay_start
 13649-13662  _restream_html_overlay_stop
 12857-12880  _restream_overlay_files
 18092-18124  _restream_platform_state
 18249-18284  _restream_resume_after_restart
 13710-13768  _restream_tts_enqueue_wav
 13420-13452  _restream_tts_feeder
 13417-13418  _restream_tts_fifo_path
 13665-13692  _restream_tts_start
 13694-13708  _restream_tts_stop
 18130-18246  _restream_verify_loop
 22339-22351  _retention_loop
 22333-22336  _retention_scan
  2551-2553   _room_is_abo
  5640-5757   _run_ai_call
 12166-12179  _run_async_from_flask
 19660-19663  _run_priv
 26135-26143  _run_selfcheck_and_exit
 22354-22365  _s3_client
  7512-7563   _safe_send
  4619-4635   _sample_net_throughput
  2499-2526   _schedule_next_check
 22287-22330  _scheduler_loop
  3981-3985   _schema_pk
 12183-12188  _scraper_session
 24031-24070  _screen_full
 11366-11403  _sec_headers
  2219-2221   _select_stream_from_data_section
 25948-26132  _selfcheck
  8304-8338   _send_live_notice
  1270-1274   _should_defer_upload
 22773-22808  _shrink_for_discord
  9979-9991   _sicheres_ziel
 25328-25345  _sign_health_check
 25348-25367  _sign_health_loop
  7372-7383   _spawn
 26407-26437  _spawn_from_flask
 19942-19945  _st_befund
 17430-17671  _start_chat_listener
 12146-12163  _start_loop_watchdog
 11195-11223  _stats_loop
 11174-11177  _stats_output_path
 11180-11192  _stats_write
  8032-8048   _storage_cleanup_loop
 25387-25394  _story_for
  3258-3264   _stream_url_expiry
  3273-3279   _stream_url_is_fresh
  3266-3271   _stream_url_ttl
 15558-15565  _streamer_persona_get
 13369-13373  _studio_chain
 22471-22593  _system_backup
 22602-22632  _system_backup_loop
 10379-10418  _test_proxy
 10925-10941  _testpush_resolve_live
  7488-7509   _tg_sprache_setzen
  8211-8221   _tg_topics_load_into_mem
  8208-8209   _tg_topics_path
  8223-8230   _tg_topics_save
  9787-9795   _token_ok
  8233-8237   _topic_forget
 12459-12470  _tracking_max_duration
  4245-4259   _tracking_remove_cleanup
  4276-4288   _tracking_resume_cleanup
  1504-1527   _try_attach_file_handler
 19145-19153  _tts_cleanup
 10901-10905  _tunnel_effective
 18641-18694  _twitch_channel_status
 24073-24218  _twitch_chat_loop
 23887-23990  _twitch_eventsub_loop
  1293-1306   _upload_queue_add
  1317-1319   _upload_queue_count
  1276-1285   _upload_queue_load
  1266-1268   _upload_queue_path
  1308-1315   _upload_queue_remove
  1287-1291   _upload_queue_save
  1321-1362   _upload_window_loop
  7236-7243   _uptime_s
 12834-12843  _url_host
   735-752    _url_ohne_zugang
   820-824    _usage_record_claude
  7426-7470   _verbindung_verloren
  6373-6404   _viewer_sample_loop
  9876-9879   _wants_html
  7246-7260   _warn_empty_env
 25117-25238  _watchdog_loop
 23626-23634  _wchat_thank_ok
 17264-17294  _whisper_get_model
  7333-7340   _whisper_native_section
 16465-16471  _whisper_pool
 17363-17392  _whisper_segments
 17296-17360  _whisper_transcribe
 13200-13362  _write_restream_overlay
 13162-13197  _write_restream_overlay_async
 24242-24322  _youtube_api_chat_loop
 18697-18800  _youtube_api_status
 18803-18870  _youtube_channel_status
 24325-24486  _youtube_chat_loop
 23486-23499  _youtube_restream_autoconfig
 23502-23526  _youtube_restream_autoconfig_inner
 23593-23621  _youtube_send
 18938-18979  _youtube_set_channel
 23529-23563  _yt_access_token
 23566-23581  _yt_live_chat_id
 23589-23590  _yt_sendrate_cfg
 24221-24236  _yt_timeout
  2790-2791   _ytdlp_detect_available
  2793-2804   _ytdlp_note_result
 12033-12035  _zombie_child_count
  7112-7136   about
  4156-4160   add_ai_log_entry
  4073-4076   add_archive_entry
  4657-4659   add_archive_rule
  4447-4481   add_recording
  4220-4237   add_tracking
  5760-5793   ai
  3808-3859   ai_chat
  3893-3903   ai_history_append
  3905-3910   ai_history_clear
  3882-3891   ai_history_load
  3867-3880   ai_rate_limit_check
  5822-5830   aireset
 16800-16819  azrael_chat
 24491-24613  brain_cmd
  3282-3466   build_recording_cmd
  4240-4243   bulk_add_trackings
  6609-6668   bulkadd
  8051-8191   check_all_trackings
  4292-4304   claim_live_transition
 15635-16397  class KickModerator
 13981-15398  class RestreamManager
 10784-10826  classify_proxy_anonymity
  5868-6066   cleanup
  4907-4913   cleanup_old_recordings
  4438-4445   clear_recording
 23243-23308  clip_moment
  4609-4612   compute_storage_forecast
  6731-6775   cookies_cmd
  4211-4217   count_trackings_for_chat
  4143-4154   decide_preferred_recorder
  4083-4086   delete_archive_entry
  4661-4663   delete_archive_rule
  5297-5444   diag
 24725-24786  einnahmen_cmd
  4603-4606   find_recordings_by_fingerprint
  4104-4120   finish_recording_attempt
  4264-4266   get_all_active_trackings
  4171-4173   get_all_checks
  4483-4486   get_all_recordings
  4552-4554   get_all_tags_with_counts
  4580-4583   get_annotations_for_recording
  4078-4081   get_archive_entry
  4573-4576   get_bookmarked_recordings
  1984-2101   get_cookie_health
  4540-4546   get_event_log
  4127-4141   get_last_recording_attempt
  2871-2976   get_live_status
  4846-4849   get_manual_recordings
  4588-4591   get_or_compute_inspect_sync
  4948-4951   get_outcome_breakdown
  4559-4562   get_priority_poll_interval
  4122-4125   get_recent_recording_attempts
  4488-4491   get_recording_by_id
  4566-4569   get_recording_note
  3600-3623   get_redis
  4200-4203   get_stats
  4901-4905   get_storage_stats
  4681-4683   get_tiktok_status_distribution
  4306-4315   get_tracking_state
  4261-4262   get_trackings_for_group
  4862-4865   get_trash_recordings
  8959-9622   handle_recording_finished
  4003-4028   init_db
  4653-4655   list_archive_rules
  5101-5139   live
  7566-7574   live_check_worker
  3678-3712   llm_chat
  3735-3763   llm_chat_sync
  3720-3732   llm_list_models
  4499-4532   log_event
  1572-1605   log_recording_failure
  6925-6974   logs_cmd
 25435-25938  main
  5796-5819   on_ai_media
  7051-7077   on_ai_reply
  7080-7109   on_azrael_mention
  7141-7171   on_callback
 16825-16929  oracle_handle
  6814-6817   pause_tracking
  4961-4966   profile_keyboard
  6876-6922   quota
  7955-8029   reaper_loop
  4677-4679   record_tiktok_status
  5835-5865   recstatus
  3625-3633   redis_get_json
  3636-3642   redis_set_json
 24789-24799  report_cmd
 10829-10831  report_proxy_result
  2333-2360   resolve_tiktok_live_stream
  4857-4860   restore_recording
  6820-6823   resume_tracking
  4666-4671   run_archive_rules
 24802-25024  run_bot
 11953-12000  run_flask
  4641-4644   sample_bandwidth_for_active
  4163-4169   save_tiktok_check
  4430-4436   set_recording_file
  4269-4273   set_tracking_paused
  4852-4855   soft_delete_recording
  8344-8957   split_and_send_video
  5014-5056   start
  4088-4102   start_recording_attempt
  6069-6107   stats
  4827-4844   stop_manual_recording
  6826-6873   stoprec
  6297-6305   summary_cmd
  6977-7048   sysres
  5446-5590   teststream
  5058-5099   tiktok
  6671-6728   topusers
  5176-5233   track
  5141-5173   track_exact
  5247-5295   tracklist
  4693-4825   trigger_manual_recording
  4391-4428   try_acquire_recording_lock
  4868-4870   universal_search
  5235-5245   untrack
 24616-24722  update_cmd
  4598-4601   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, get_archive_entries_paged, get_archive_entry, run_archive_file_check
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            config, configure
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, fehlgrund, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_region, s3_zugang, sys_backup, sys_hour, sys_keep, sys_max_file_mb
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
binresolve.py          resolve
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookies.py             —
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_async, db_conn, get_pool, set_pool
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordlimits.py       describe, effective_upload_mb, gate_mb, guild_limit_mb
discordstate.py        invite, state_get
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventlog.py            leeren, schreibe, stand
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      drawtext_chain, studio_chain
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, last_errors, list_models_sync
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
highlights.py          check, new_state, observe, score, zustand
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             broadcaster_id, configure, oauth_exchange, slug
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
outcomes.py            get_outcome_breakdown
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, fenstergroesse, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             cleanup, forecast, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
twitchoauth.py         access_token, authorize_url, configure, exchange_code, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             changelog, current, latest, summary_line
whispercfg.py          geladen, name, verfuegbar, waehle
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status
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
