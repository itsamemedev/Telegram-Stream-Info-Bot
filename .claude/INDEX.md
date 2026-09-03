# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (89)

```
 10452  GET              /                                                dashboard
 13226  GET              /api/abo/status                                  api_abo_status
 10525  GET              /api/active-recordings                           api_active_recordings
 13297  GET              /api/activity-pulse                              api_activity_pulse
 13104  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 13170  GET/POST         /api/auto-archive-rules                          api_archive_rules
 13194  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 13198  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 11580  GET              /api/automation/status                           api_automation_status
 11602  POST             /api/automation/toggle                           api_automation_toggle
 10824  GET              /api/backoff-watch                               api_backoff_watch
 12664  POST             /api/backup/run                                  api_backup_run
 12630  GET              /api/backup/status                               api_backup_status
 12619  POST             /api/backup/system                               api_backup_system
 13136  GET              /api/bandwidth/live                              api_bandwidth_live
 13089  GET              /api/bookmarks                                   api_bookmarks_list
 20043  GET              /api/channel/categories                          api_channel_categories
 20049  POST             /api/channel/set                                 api_channel_set
 19896  GET              /api/channels/status                             api_channels_status
 10506  GET              /api/checks                                      api_checks
 19570  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 19553  GET              /api/clips                                       api_clips
 19599  POST/DELETE      /api/clips/clear                                 api_clips_clear
 13605  GET              /api/community/stats                             api_community_stats
 20480  GET              /api/data/export                                 api_data_export
 19468  GET              /api/debug/threads                               api_debug_threads
 21327  GET              /api/defense/attacks                             api_defense_attacks
 21294  GET              /api/defense/crowdsec                            api_defense_crowdsec
 21312  GET              /api/defense/fail2ban                            api_defense_fail2ban
 21018  GET              /api/defense/overview                            api_defense_overview
 13118  GET              /api/events                                      api_events
 12501  GET              /api/events/stream                               api_events_stream
 13131  GET              /api/forecast/storage                            api_forecast_storage
 11618  GET              /api/freeai/status                               api_freeai_status
 12090  GET              /api/health                                      api_health
 13149  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 13145  GET              /api/heatmap/recordings                          api_heatmap_recordings
 19500  GET              /api/highlights                                  api_highlights
 19512  POST             /api/highlights/config                           api_highlights_config
 10386  POST             /api/login                                       dashboard_login_submit
 13590  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 13559  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 12399  GET              /api/notify/status                               api_notify_status
 12410  POST             /api/notify/test                                 api_notify_test
 10610  GET              /api/outcomes                                    api_outcomes
 10643  GET              /api/profile/<username>                          api_profile
 13315  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 13157  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 13280  GET              /api/proxy/heatmap                               api_proxy_heatmap
 13257  GET              /api/proxy/trend                                 api_proxy_trend
 11956  GET              /api/public/stats                                api_public_stats
 10486  GET              /api/pulse                                       api_pulse
 12723  GET              /api/recording-attempts                          api_recording_attempts
 12448  GET              /api/retention/preview                           api_retention_preview
 12457  POST             /api/retention/run                               api_retention_run
 13074  GET              /api/search                                      api_search
 21065  GET              /api/selftest                                    api_selftest
 19306  GET              /api/shield/stats                                api_shield_stats
 10547  GET              /api/storage                                     api_storage
 10554  POST             /api/storage/cleanup                             api_storage_cleanup
 13211  GET              /api/stream/inspect/<username>                   api_stream_inspect
 11546  GET              /api/stream/timeline                             api_stream_timeline
 12151  GET              /api/stream/transcript                           api_stream_transcript
 10578  GET              /api/summary/preview                             api_summary_preview
 12788  GET              /api/system                                      api_system
 13638  GET              /api/system/check_timing                         api_check_timing
 13730  GET              /api/system/config_drift                         api_config_drift
 12165  GET              /api/system/config_snapshot                      api_system_config_snapshot
 12257  GET              /api/system/preflight                            api_system_preflight
 12383  GET              /api/system/preflight_history                    api_system_preflight_history
 12566  GET              /api/system/resilience                           api_system_resilience
 13109  GET              /api/tags                                        api_tags_list
 10520  GET              /api/top                                         api_top
 10879  GET              /api/trend-7d                                    api_trend_7d
 19619  GET              /api/tts/<fn>                                    api_tts_file
 20345  GET              /api/upload_window                               api_upload_window
 10624  GET              /api/userstats                                   api_userstats
 12004  GET              /api/version                                     api_version
 12761  GET              /archive/<int:eid>/download                      archive_download
 12818  GET              /download/<int:recording_id>                     download
 12701  GET              /health                                          health
 19437  GET              /healthz                                         healthz
 10377  GET              /login                                           dashboard_login_page
 10407  GET              /logout                                          dashboard_logout
 10414  GET              /manifest.webmanifest                            pwa_manifest
 12193  GET              /metrics                                         api_prometheus_metrics
 20318  GET              /overlay                                         overlay_page
 10438  GET              /pwa-icon-<variant>.png                          pwa_icon
 10424  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (270)

```
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
   184  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   121  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   106  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    83  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   144  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    70  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    72  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    44  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
    31  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    43  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    42  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    77  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   112  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   274  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   259  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   182  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
    60  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    67  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   203  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   230  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   190  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
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
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
    64  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    53  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   211  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
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
   210  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   193  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
    94  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   823  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   905  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   933  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   944  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   810  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   872  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   859  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   840  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
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
   315  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   305  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   340  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    56  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    77  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    43  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
    93  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   118  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   209  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   204  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   264  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
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
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
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
```

## Discord-Slash-Commands (45)

```
 21791  /ai                     
 22250  /ask                    
 21882  /assign_role            
 21928  /ban                    
 22582  /botstats               
 22506  /clearwarns             
 22546  /clip                   
 22531  /clipoftheweek          
 22373  /clips                  
 21843  /create_category        
 21812  /create_channel         
 21871  /create_group           
 21854  /create_role            
 21828  /create_voice           
 22164  /daily                  
 22280  /event                  
 22323  /events                 
 22419  /follow                 
 22403  /help                   
 21917  /kick                   
 22146  /leaderboard            
 22359  /livenow                
 22389  /post_test              
 22220  /profile                
 21952  /purge                  
 22132  /rank                   
 22346  /recstatus              
 21893  /remove_role            
 21805  /restream_status        
 21904  /set_channel_perms      
 22097  /setup_community        
 22115  /setup_targets          
 22445  /stats                  
 21717  /status                 
 22741  /streaminfo             
 22638  /sys_report             
 22614  /sys_unpause            
 21939  /timeout                
 22517  /topstreamers           
 21747  /track                  
 21731  /tracklist              
 22434  /unfollow               
 21780  /untrack                
 22467  /warn                   
 22491  /warnings               
```

## Discord-Events (4)

```
 23227  on_member_join
 23189  on_message
 22828  on_raw_reaction_add
 23262  on_ready
```

## Top-Level-Symbole in bot.py (483 Funktionen, 2 Klassen)

```
  2522-2523   _abo_key
  2543-2561   _abo_probe_dump
 20587-20597  _active_recorder_sync
 16571-16578  _ad_allowlist
 17712-17718  _agent_for
 20599-20617  _ai_calls_total_sync
 17721-17737  _ai_telemetry
 18226-18244  _alert
 23378-23428  _alert_monitor_loop
 23809-23871  _announce_loop
  3464-3467   _anthropic_key
  3474-3476   _anthropic_model
 10130-10133  _arg_int
  2514-2519   _as_dict
 18380-18402  _audio_tap_cmd
 10298-10309  _auth_cookie
 10265-10294  _auth_guard
  1670-1675   _auto_on
 19272-19290  _auto_restream_loop
 24922-24937  _azrael_broadcast_reply
 24822-24844  _azrael_chat_reply
 24805-24819  _azrael_chat_should_reply
 24850-24852  _azrael_gate_cfg
 17742-17756  _azrael_live_state
 20230-20244  _azrael_overlay_state
 18108-18162  _azrael_proactive_loop
 17560-17616  _azrael_reaction_to_chats
 24855-24862  _azrael_reply_all_chats
 24792-24802  _azrael_self_names
 24890-24919  _azrael_send_to
 17762-17783  _azrael_system
 23547-23550  _backup_active
 23628-23641  _backup_loop
 23340-23349  _brain_growth_loop
 10930-10957  _brain_growth_snapshot
  2450-2470   _brain_hint_delay
  6556-6584   _brain_notify
 12480-12497  _browser_push
  6600-6687   _build_daily_summary
  2953-3133   _build_native_cmd
 14759-14946  _build_restream_cmd
  3177-3210   _build_ytdlp_cmd
 20539-20546  _cached_probe
  5378-5405   _can_stop_tracking
  1850-1872   _capture_set_cookies
 13374-13377  _cfg_get
 13380-13382  _cfg_set
 20004-20039  _channel_set_all
 14002-14005  _chat_connected
 14008-14024  _chat_disconnected
  8621-8632   _chat_is_forum
 14044-14046  _chat_sanitize
 13987-13999  _chat_stat
 14027-14030  _chat_stats_snapshot
  3740-3751   _check_ai_alive_sync
  3754-3766   _check_ai_models_sync
 20548-20561  _check_redis_alive_sync
 20563-20583  _check_redis_version_sync
 11225-11268  _classify_pool_anonymity
 11271-11288  _classify_pool_anonymity_bg
   821-825    _claude_chat_sync_metered
 10159-10166  _client_ip
 23903-23930  _clip_prune
 23933-23943  _clip_recfile_for
 24456-24462  _clip_should_velocity
 23984-24066  _clip_to_discord
  3638-3647   _close_ai_session
 24968-24983  _cohost_broadcast
 24953-24954  _cohost_cfg
 25009-25021  _cohost_fire_highlight
 24957-24965  _cohost_gate
 24986-25006  _cohost_highlight
 24115-24149  _community_events_loop
 10778-10780  _conv_messages
  6964-7007   _cookie_alarm_loop
  1922-1926   _cookie_autorefresh_info
  1827-1831   _cookie_header
 12530-12562  _cpu_load_snapshot
  3960-3972   _create_index_safe
 20820-20926  _crowdsec_status
 20766-20817  _crowdsec_via_lapi
 20631-20649  _cscli_bin
 20655-20668  _cscli_path
  6854-6879   _daily_summary_loop
 20686-20703  _darf_journal_lesen
 23352-23375  _db_maintenance_loop
  6823-6851   _db_vacuum_loop
 16594-16618  _detect_foreign_ad
  1408-1419   _diag_path_owner
 18014-18058  _director_finalize
 18826-18833  _director_for
 17963-18011  _director_mark
 24350-24385  _disc_automod_check
 24326-24329  _disc_state_get
 24332-24339  _disc_state_set
 21369-21382  _discord_guild_filesize_bytes
 21574-21578  _discord_invite
 24287-24323  _discord_live_thread
 18165-18177  _discord_notify
 21473-21498  _discord_ops_alert
 24185-24283  _discord_post_user
 21634-23337  _discord_run_once
 21513-21571  _discord_start
 23874-23880  _discord_stop
 21390-21392  _discord_upload_limit_label
 21385-21387  _discord_upload_limit_mb
  6882-6959   _disk_alarm_loop
 26401-26450  _disk_autoclean
 26453-26466  _disk_guard_loop
 26393-26398  _disk_pct
 14352-14354  _drawtext_chain
 12917-12919  _dump_all_threads
 11150-11214  _enrich_proxies_with_geo
  2067-2111   _ensure_cookie_file_netscape
 21581-21631  _ensure_discord_invite
 24080-24112  _ensure_error_channel
  8680-8683   _ensure_notify_topic
 11395-11432  _ensure_proxy_ready
  8634-8661   _ensure_topic
   678-680    _env_int
   683-685    _env_int_range
 24152-24182  _error_channel_loop
 18210-18223  _event_webhook
 13817-13830  _evolution_loop
  5998-6032   _extract_file_payload
  2199-2201   _extract_urls_from_streamurl_node
 20671-20678  _f2b_sudo_hint
 18246-18248  _faster_whisper_available
 11039-11057  _fetch_proxy_list
 18660-18688  _fetch_tiktok_room_id
   754-757    _ff_cmd
 14518-14523  _find_chromium
  3170-3174   _find_external_recorder
  2204-2206   _find_stream_urls
 13425-13450  _fire_webhooks
  7743-7752   _fork_safe
   836-845    _freeai_chat_sync_metered
 20721-20763  _geo_lookup_ips
  3626-3635   _get_ai_session
  7577-7617   _get_live_info
  2740-2747   _get_resolve_semaphore
  7976-8342   _handle_single_tracking
 26219-26221  _hb
 26224-26241  _hb_while
 14053-14055  _highlight_cfg
 14058-14087  _highlight_observe
 14526-14544  _htmlov_screenshot_cmd
 18404-18414  _httpx_proxy
 13458-13470  _in_quiet_hours
 27292-27323  _install_fast_eventloop
 10025-10079  _install_fast_json
 12922-12938  _install_faulthandler
 19345-19354  _intel_ensure_schema
 19392-19427  _intel_index_loop
 19366-19376  _intel_index_one
 19357-19363  _intel_semantic
  5367-5376   _is_authorized
  7877-7883   _is_dead
  2189-2191   _is_hevc
 20706-20712  _is_private_ip
  1572-1579   _is_process_running
  6586-6597   _is_quiet_hours
  1209-1218   _is_upload_window
 10114-10127  _json_error_handler
  6809-6810   _kick_broadcaster_id
  6721-6763   _kick_follower_count
  6705-6708   _kick_slug
 12031-12062  _kick_user_token
  4009-4012   _kind_from_filename
 13487-13492  _latest_popularity
 19041-19074  _live_react_loop
 18837-19030  _live_react_worker
 17619-17630  _live_transcript_push
 19032-19039  _live_users
 18061-18105  _living_title_loop
  1748-1821   _load_cookies_dict
 23553-23625  _local_backup_scan
 10096-10110  _log_5xx
 14954-14966  _looks_like_codec_err
 14949-14951  _looks_like_source_expired
  7793-7823   _loop_fehler
 12942-12951  _loop_heartbeat
 26189-26216  _loop_lag_monitor
 12954-13022  _loop_watchdog_thread
 17499-17513  _loyalty_add
 17490-17496  _loyalty_get
 17516-17524  _loyalty_top
 13624-13626  _manual_donations_total
  7885-7886   _mark_dead
 11709-11725  _marketing_loop
 24869-24887  _maybe_handle_command
 26552-26576  _maybe_hype_clip
  3927-3950   _migrate_columns
 25148-25159  _mod_is_exempt
 25162-25167  _mod_warn_first
 25170-25173  _mod_warn_text
 13857-13865  _modlog
   960-962    _multistream_targets
  7755-7756   _nc_create_subprocess_exec
  7759-7760   _nc_create_subprocess_shell
 11961-11978  _news_loop
 13884-13886  _normalize_ingest
  2381-2398   _note_check_duration
  8674-8677   _notify_topic_name
 17645-17653  _oracle_memories
 17918-17952  _oracle_memorize
 17656-17669  _oracle_persona
 17638-17642  _oracle_recent_text
 14178-14186  _ov_atomic_write
 14166-14172  _ov_bar
 16497-16509  _ov_clip_text
 14175-14176  _ov_oneline
 20282-20311  _overlay_push
 14472-14515  _overlay_render_size
 13950-13954  _overlay_session_reset
 20246-20249  _overlay_src_ok
 16581-16591  _own_invites
 14467-14469  _parse_size
 20934-21014  _parse_ssh_attacks
  7179-7212   _pause_resume_cmd
  1876-1920   _persist_refreshed_cookies
  1714-1746   _pick_checked_pull_proxy
 10195-10208  _pin_auth_value
 10254-10255  _pin_clear_fail
 10234-10237  _pin_locked
 10240-10251  _pin_note_fail
 10211-10231  _pin_ok
 20140-20165  _piper_pick_model
 20177-20224  _piper_say
 13387-13422  _post_json_threaded
 14446-14464  _probe_video_size
  1600-1617   _proc_is_recorder
 11137-11148  _proxy_geo_cache_put
 11364-11392  _proxy_pool_refresh_loop
  1680-1711   _proxy_report_recording
 12907-12909  _prune_stall_dumps
 11779-11900  _public_stats
 18181-18207  _push_notify
 10356-10358  _pwa_dir
 11108-11123  _quick_validate_proxy
 13453-13455  _quiet_hours_config
 10321-10354  _rate_guard
 17464-17470  _react_warn
  7663-7702   _reap_proc
  2421-2443   _record_check_outcome
   749-751    _redact_stream_urls
 11291-11361  _refresh_proxy_pool
  2215-2305   _resolve_via_html
  2563-2717   _resolve_via_webcast_api_v2
  2780-2842   _resolve_via_ytdlp
 24496-24625  _resolve_youtube_ingest
 13933-13944  _restream_active_sources
 18691-18790  _restream_chat_guardian
 14090-14162  _restream_chat_push
 14547-14634  _restream_html_overlay_start
 14637-14650  _restream_html_overlay_stop
 13895-13918  _restream_overlay_files
 19078-19110  _restream_platform_state
 19234-19269  _restream_resume_after_restart
 14698-14756  _restream_tts_enqueue_wav
 14408-14440  _restream_tts_feeder
 14405-14406  _restream_tts_fifo_path
 14653-14680  _restream_tts_start
 14682-14696  _restream_tts_stop
 19116-19231  _restream_verify_loop
 23518-23530  _retention_loop
 23477-23515  _retention_scan
  2525-2527   _room_is_abo
  6036-6153   _run_ai_call
 13045-13058  _run_async_from_flask
 20715-20718  _run_priv
 27280-27288  _run_selfcheck_and_exit
 23533-23544  _s3_client
  7912-7963   _safe_send
  4631-4647   _sample_net_throughput
  2473-2500   _schedule_next_check
 23431-23474  _scheduler_loop
  3953-3957   _schema_pk
 13062-13067  _scraper_session
 25176-25215  _screen_full
 12106-12143  _sec_headers
  2194-2196   _select_stream_from_data_section
 27093-27277  _selfcheck
  8686-8720   _send_live_notice
  1232-1236   _should_defer_upload
 23946-23981  _shrink_for_discord
 10361-10373  _sicheres_ziel
 26473-26490  _sign_health_check
 26493-26512  _sign_health_loop
  7772-7783   _spawn
 27552-27582  _spawn_from_flask
 21058-21061  _st_befund
 18416-18657  _start_chat_listener
 13025-13042  _start_loop_watchdog
 11924-11952  _stats_loop
 11903-11906  _stats_output_path
 11909-11921  _stats_write
  8414-8430   _storage_cleanup_loop
 26532-26539  _story_for
  3232-3238   _stream_url_expiry
  3247-3253   _stream_url_is_fresh
  3240-3245   _stream_url_ttl
 16544-16551  _streamer_persona_get
 14357-14361  _studio_chain
 23650-23772  _system_backup
 23775-23805  _system_backup_loop
 11060-11099  _test_proxy
 11657-11673  _testpush_resolve_live
  7888-7909   _tg_sprache_setzen
  8593-8603   _tg_topics_load_into_mem
  8590-8591   _tg_topics_path
  8605-8612   _tg_topics_save
 10169-10177  _token_ok
  8615-8619   _topic_forget
 13473-13484  _tracking_max_duration
  4218-4232   _tracking_remove_cleanup
  4249-4261   _tracking_resume_cleanup
  1466-1489   _try_attach_file_handler
 20167-20175  _tts_cleanup
 11633-11637  _tunnel_effective
 19663-19716  _twitch_channel_status
 25218-25363  _twitch_chat_loop
 25032-25135  _twitch_eventsub_loop
  1255-1268   _upload_queue_add
  1279-1281   _upload_queue_count
  1238-1247   _upload_queue_load
  1228-1230   _upload_queue_path
  1270-1277   _upload_queue_remove
  1249-1253   _upload_queue_save
  1283-1324   _upload_window_loop
  7636-7643   _uptime_s
 13872-13881  _url_host
   729-746    _url_ohne_zugang
   814-818    _usage_record_claude
  7826-7870   _verbindung_verloren
  6766-6797   _viewer_sample_loop
  6813-6820   _viewer_stats
 10258-10261  _wants_html
  7646-7660   _warn_empty_env
 26262-26383  _watchdog_loop
 24771-24779  _wchat_thank_ok
 18250-18280  _whisper_get_model
  7733-7740   _whisper_native_section
 17451-17457  _whisper_pool
 18349-18378  _whisper_segments
 18282-18346  _whisper_transcribe
 14188-14350  _write_restream_overlay
 25387-25467  _youtube_api_chat_loop
 19719-19822  _youtube_api_status
 19825-19892  _youtube_channel_status
 25470-25631  _youtube_chat_loop
 24631-24644  _youtube_restream_autoconfig
 24647-24671  _youtube_restream_autoconfig_inner
 24738-24766  _youtube_send
 19960-20001  _youtube_set_channel
 24674-24708  _yt_access_token
 24711-24726  _yt_live_chat_id
 24734-24735  _yt_sendrate_cfg
 25366-25381  _yt_timeout
  2764-2765   _ytdlp_detect_available
  2767-2778   _ytdlp_note_result
 12912-12914  _zombie_child_count
  7513-7537   about
  4128-4132   add_ai_log_entry
  4045-4048   add_archive_entry
  4744-4759   add_archive_rule
  4420-4454   add_recording
  4193-4210   add_tracking
  6156-6189   ai
  3780-3831   ai_chat
  3865-3875   ai_history_append
  3877-3882   ai_history_clear
  3854-3863   ai_history_load
  3839-3852   ai_rate_limit_check
  6218-6226   aireset
 17786-17805  azrael_chat
 25636-25758  brain_cmd
  3256-3440   build_recording_cmd
  4213-4216   bulk_add_trackings
  7010-7069   bulkadd
  8433-8573   check_all_trackings
  4265-4277   claim_live_transition
 16621-17383  class KickModerator
 14969-16384  class RestreamManager
 11478-11520  classify_proxy_anonymity
  6264-6462   cleanup
  5227-5268   cleanup_old_recordings
  4411-4418   clear_recording
 24388-24453  clip_moment
  4575-4624   compute_storage_forecast
  7132-7176   cookies_cmd
  4184-4190   count_trackings_for_chat
  4115-4126   decide_preferred_recorder
  4055-4058   delete_archive_entry
  4761-4769   delete_archive_rule
  5693-5840   diag
 25870-25931  einnahmen_cmd
  4569-4572   find_recordings_by_fingerprint
  4076-4092   finish_recording_attempt
  4237-4239   get_all_active_trackings
  4143-4146   get_all_checks
  4456-4459   get_all_recordings
  4518-4520   get_all_tags_with_counts
  4546-4549   get_annotations_for_recording
  4050-4053   get_archive_entry
  4539-4542   get_bookmarked_recordings
  1943-2060   get_cookie_health
  4506-4512   get_event_log
  4099-4113   get_last_recording_attempt
  2845-2950   get_live_status
  5027-5030   get_manual_recordings
  4554-4557   get_or_compute_inspect_sync
  5303-5347   get_outcome_breakdown
  4525-4528   get_priority_poll_interval
  4722-4731   get_profile_snapshots
  4094-4097   get_recent_recording_attempts
  4461-4464   get_recording_by_id
  4532-4535   get_recording_note
  3574-3597   get_redis
  4173-4176   get_stats
  5194-5225   get_storage_stats
  4862-4864   get_tiktok_status_distribution
  4279-4288   get_tracking_state
  4234-4235   get_trackings_for_group
  5043-5046   get_trash_recordings
  9341-10004  handle_recording_finished
  3975-4000   init_db
  5117-5171   inspect_stream_url
  4734-4742   list_archive_rules
  5497-5535   live
  7966-7974   live_check_worker
  3650-3684   llm_chat
  3707-3735   llm_chat_sync
  3692-3704   llm_list_models
  4472-4498   log_event
  1534-1567   log_recording_failure
  7326-7375   logs_cmd
 26580-27083  main
  6192-6215   on_ai_media
  7452-7478   on_ai_reply
  7481-7510   on_azrael_mention
  7542-7572   on_callback
 17811-17915  oracle_handle
  7215-7218   pause_tracking
  5357-5362   profile_keyboard
  7277-7323   quota
  8344-8411   reaper_loop
  4858-4860   record_tiktok_status
  6231-6261   recstatus
  3599-3607   redis_get_json
  3609-3615   redis_set_json
 25934-25944  report_cmd
 11523-11525  report_proxy_result
  2308-2335   resolve_tiktok_live_stream
  5038-5041   restore_recording
  7221-7224   resume_tracking
  4772-4852   run_archive_rules
 25947-26169  run_bot
 12832-12879  run_flask
  4650-4695   sample_bandwidth_for_active
  4701-4720   save_profile_snapshot
  4135-4141   save_tiktok_check
  4403-4409   set_recording_file
  4242-4246   set_tracking_paused
  5033-5036   soft_delete_recording
  8726-9339   split_and_send_video
  5410-5452   start
  4060-4074   start_recording_attempt
  6465-6503   stats
  5008-5025   stop_manual_recording
  7227-7274   stoprec
  6690-6698   summary_cmd
  7378-7449   sysres
  5842-5986   teststream
  5454-5495   tiktok
  7072-7129   topusers
  5572-5629   track
  5537-5569   track_exact
  5643-5691   tracklist
  4874-5006   trigger_manual_recording
  4364-4401   try_acquire_recording_lock
  5049-5108   universal_search
  5631-5641   untrack
 25761-25867  update_cmd
  4564-4567   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, get_archive_entries_paged, get_archive_entry, run_archive_file_check
archivename.py         open_unique
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            config, configure
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
binresolve.py          resolve
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, live_ping, note_chatter, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookies.py             —
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_conn, get_pool, set_pool
director.py            class LiveDirector, configure
discordlimits.py       describe, effective_upload_mb, gate_mb, guild_limit_mb
discordstate.py        invite, state_get
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
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
highlights.py          check, new_state, observe, score
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             broadcaster_id, configure, oauth_exchange, slug
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls
loyalty.py             award_chat, award_return, configure, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
recdb.py               configure, find_recordings_by_fingerprint, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
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
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tiktokcheck.py         account_exists, configure
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
